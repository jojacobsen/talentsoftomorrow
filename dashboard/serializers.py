import uuid
from dateutil.relativedelta import relativedelta
import random
import json
import decimal
from rest_framework import serializers, exceptions
from dashboard.models import Performance, Player, Coach, Club, Measurement, ProfilePicture, Unit, \
    DnaResult, DnaMeasurement, PerformanceAnalyse
from django.contrib.auth.models import User, Group
from dashboard.utils import RscriptAnalysis


def create_username(last_name, first_name):
    username = first_name[:1].lower() + last_name[:3].lower() + str(random.randrange(10000, 100001, 2))
    ''.join(e for e in username if e.isalnum())

    while User.objects.filter(username=username).exists():
        username = first_name[:1].lower() + last_name[:3].lower() + str(random.randrange(10000, 100001, 2))
        ''.join(e for e in username if e.isalnum())

    return username


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicture


class CurrentUserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    profilepicture = ProfilePictureSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'is_superuser', 'is_staff', 'is_active', 'username', 'first_name', 'last_name',
                  'email', 'groups', 'date_joined', 'last_login', 'profilepicture')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'email')


class NewUserSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(allow_blank=False, max_length=200, required=True)
    first_name = serializers.CharField(allow_blank=False, max_length=200, required=True)

    class Meta:
        model = User
        fields = ('last_name', 'first_name')


class ClubSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Club


class CoachSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Coach
        fields = ('id', 'club', 'user')


class PlayersSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ('id', 'user', 'lab_key', 'gender', 'birthday', 'first_name', 'last_name', 'active', 'archived')


class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ('id', 'user', 'lab_key', 'gender', 'birthday', 'club', 'first_name', 'last_name', 'active', 'archived')


class CurrentClubSerializer(serializers.ModelSerializer):
    user = CurrentUserSerializer(read_only=True)

    class Meta:
        model = Club


class CurrentCoachSerializer(serializers.ModelSerializer):
    user = CurrentUserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Coach
        fields = ('id', 'club', 'user')


class CurrentPlayerSerializer(serializers.ModelSerializer):
    user = CurrentUserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ('id', 'user', 'club', 'gender', 'birthday', 'first_name', 'last_name')


class NewPlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        exclude = ('user', 'lab_key', 'club')

    def validate(self, data):
        group = self.context['request'].user.groups.values_list('name', flat=True)

        if 'Club' in group:
            return data
        elif 'Coach' in group:
            return data
        elif 'Player' in group:
            raise exceptions.PermissionDenied('Players can not create new users.')
        else:
            raise exceptions.PermissionDenied('User group not selected.')

    def create(self, validated_data):
        # Check the group of the current user
        group = self.context['request'].user.groups.values_list('name', flat=True)
        if 'Club' in group:
            validated_data['club'] = self.context['request'].user.club
        elif 'Coach' in group:
            validated_data['club'] = self.context['request'].user.coach.club

        # Create the user for the player
        username = create_username(last_name=validated_data['last_name'], first_name=validated_data['first_name'])
        user = User.objects.create_user(username=username)
        # Add the group
        player_group = Group.objects.get(name='Player')
        user.groups.add(player_group)
        validated_data['user'] = user
        validated_data['lab_key'] = str(uuid.uuid5(uuid.NAMESPACE_X500, user.username))

        # Create the player
        player = Player.objects.create(**validated_data)
        return player


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance

    def validate(self, data):
        group = self.context['request'].user.groups.values_list('name', flat=True)

        if 'Club' in group:
            if data['player'].club != self.context['request'].user.club:
                raise exceptions.PermissionDenied('Club has no permission to access performance data of player.')
        elif 'Coach' in group:
            if data['player'].club != self.context['request'].user.coach.club:
                raise exceptions.PermissionDenied('Coach has no permission to access performance data of player.')
        elif 'Player' in group:
            raise exceptions.PermissionDenied('Players can not post performance data.')
        else:
            raise exceptions.PermissionDenied('User group not selected.')

        if not (data['measurement'].lower_limit <= data['value'] <= data['measurement'].upper_limit):
            raise serializers.ValidationError('%s is not between %s...%s %s' % (data['value'],
                                                                             data['measurement'].lower_limit,
                                                                             data['measurement'].upper_limit,
                                                                             data['measurement'].unit))
        return data

    def create(self, validated_data):
        if validated_data['measurement'].slug_name == 'height':
            if DnaResult.objects.filter(dna_measurement=validated_data['measurement'].related_dna_measurement,
                                        player=validated_data['player']):
                predicted_height = DnaResult.objects.filter(
                    dna_measurement=validated_data['measurement'].related_dna_measurement,
                    player=validated_data['player']
                ).order_by('-date').first()

                current_height = validated_data['value'] * \
                                 decimal.Decimal(validated_data['measurement'].factor_to_dna_measurement)

                r_scripts = RscriptAnalysis()
                bio_age, slope = r_scripts.get_bio_age(predicted_height.value, current_height)
                if bio_age and slope:
                    PerformanceAnalyse.objects.update_or_create(player=validated_data['player'],
                                                                defaults={
                                                                    'bio_age': bio_age,
                                                                    'slope_to_bio_age': json.dumps(slope)
                                                                })
        performance = Performance.objects.create(**validated_data)
        return performance


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit


class MeasurementSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = Measurement


class DnaMeasurementSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = DnaMeasurement


class DnaResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DnaResult


class CreateDnaResultSerializer(serializers.ModelSerializer):
    player = serializers.CharField()
    dna_measurement = serializers.CharField()

    class Meta:
        model = DnaResult
        fields = ('date', 'value', 'original_filename', 'player', 'dna_measurement', 'meta')

    def validate(self, data):
        try:
            player = Player.objects.get(lab_key=data['player'])
        except Player.DoesNotExist:
            raise exceptions.NotFound('Player not found.')

        try:
            dna_measurement = DnaMeasurement.objects.get(slug_name=data['dna_measurement'])
        except DnaMeasurement.DoesNotExist:
            raise exceptions.NotFound('Player not found.')

        data['player'] = player
        data['dna_measurement'] = dna_measurement
        return data


class PerformanceAnalyseSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        return {
            'data': obj.slope_to_bio_age,
            'player': obj.player.id,
            'type': 'spline'
        }


class PerformancesHistoricSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        results = list()
        for p in obj:
            if any(p.player.id == r['player'] for r in results):
                for r in results:
                    if p.player.id == r['player']:
                        rel = relativedelta(p.date, p.player.birthday)
                        r['data'].append((rel.years + rel.months / 12 + rel.days / 365.25, p.value))
            else:
                result = dict()
                rel = relativedelta(p.date, p.player.birthday)
                result['data'] = [(rel.years + rel.months / 12 + rel.days / 365.25, p.value)]
                result['player'] = p.player.id
                result['type'] = 'spline'
                results.append(result)

        return results
