import uuid
from dateutil.relativedelta import relativedelta
import random
from rest_framework import serializers, exceptions
from dashboard.models import Performance, Player, Coach, Club, Measurement, ProfilePicture, Unit, \
    DnaResult, DnaMeasurement, PerformanceBenchmark
from django.contrib.auth.models import User, Group


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
        fields = ('id', 'user', 'lab_key', 'gender', 'birthday', 'club', 'first_name', 'last_name', 'active',
                  'archived')


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

    def create(self, validated_data):
        dna_result = DnaResult.objects.create(**validated_data)
        return dna_result


class PerformanceAnalyseSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        dna = obj.performanceanalyse_set.filter().order_by('-created')[0]
        dna.slope_to_bio_age.sort()
        return {
            'data': dna.slope_to_bio_age,
            'player': obj.id,
            'name': obj.first_name + ' ' + obj.last_name,
            'type': 'spline'
        }


class PerformancesHistoricSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        pk = self.context['view'].kwargs['pk']
        performances = obj.performance_set.filter(measurement__id=pk)

        data = list()
        for p in performances:
            rel = relativedelta(p.date, obj.birthday)
            data.append([rel.years + rel.months / 12 + rel.days / 365.25, p.value])

        data.sort()

        return {
            'data': data,
            'player': obj.id,
            'name': obj.first_name + ' ' + obj.last_name,
            'type': 'spline'
        }


class PerformancesToBioAgeSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        pk = self.context['view'].kwargs['pk']
        p = obj.performance_set.filter(measurement__id=pk).order_by('-date')[0]
        dna = obj.performanceanalyse_set.filter().order_by('-created')[0]
        rel = relativedelta(p.date, obj.birthday)

        data = list()
        data.append({
            'x': rel.years + rel.months / 12 + rel.days / 365.25,
            'y': p.value,
            'bio_age': False,
        }
        )

        data.append({
            'x': dna.bio_age,
            'y': p.value,
            'bio_age': True,
        }
        )

        return {
            'data': data,
            'player': obj.id,
            'name': obj.first_name + ' ' + obj.last_name,
            'type': 'line'
        }


class HeightEstimationSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        m = obj.club.measurements.filter(slug_name='height')[0]
        p = obj.performance_set.filter(measurement__id=m.pk).order_by('-date')[0]
        dna = obj.dnaresult_set.filter().order_by('-date')[0]
        rel = relativedelta(p.date, obj.birthday)

        data = list()
        data.append({
            'x': rel.years + rel.months / 12 + rel.days / 365.25,
            'y': p.value,
            'predicted_height': False,
        }
        )

        data.append({
            'x': 17.5,
            'y': dna.value,
            'predicted_height': True,
        }
        )

        return {
            'data': data,
            'player': obj.id,
            'name': obj.first_name + ' ' + obj.last_name,
            'type': 'line'
        }


class PlayerProfileSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        p = obj.performance_set.filter().order_by('-date')
        tests = list()
        for performance in p:
            # TODO: there is a fast way to do it
            if any((test.measurement==performance.measurement) for test in tests):
                continue
            tests.append(performance)

        p = dict()
        for test in tests:
            try:
                b = test.performancebenchmark_set.get()
                benchmark = {
                    'real_age': b.benchmark,
                    'bio_age': b.benchmark_bio
                }
            except PerformanceBenchmark.DoesNotExist:
                benchmark = None
            previous = obj.performance_set.filter(measurement=test.measurement.id).order_by('-date')
            if len(previous) > 1:
                # TODO: what if smaller is better?
                if previous[0].value > previous[1].value:
                    progress = 'up'
                elif previous[0].value < previous[1].value:
                    progress = 'down'
                else:
                    progress = 'constant'
            else:
                progress = 'constant'

            t = {
                'value': test.value,
                'measurement': test.measurement.id,
                'name': test.measurement.name,
                'slug': test.measurement.slug_name,
                'unit': test.measurement.unit.abbreviation,
                'benchmark': benchmark,
                'progress': progress
            }

            p.setdefault(test.measurement.group, []).append(t)

        m = obj.club.measurements.filter(slug_name='height')[0]

        current_height = obj.performance_set.filter(measurement__id=m.pk).order_by('-date')[0]
        dna_height = obj.dnaresult_set.filter().order_by('-date')[0]
        b = obj.performanceanalyse_set.filter().order_by('-created')[0]
        rel = relativedelta(current_height.date, obj.birthday)

        player = {
            'player_id': obj.id,
            'player_name': obj.first_name + ' ' + obj.last_name,
            'lab_key': obj.lab_key,
            'gender': obj.gender,
            'birthday': obj.birthday,
            'current_height': current_height.value,
            'predicted_height': dna_height.value,
            'height_unit': current_height.measurement.unit.abbreviation,
            'bio_age': b.bio_age,
            'real_age': rel.years + rel.months / 12 + rel.days / 365.25
        }
        return {
            'data': p,
            'player': player,
        }
