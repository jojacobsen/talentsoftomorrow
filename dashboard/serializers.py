import uuid
import random
from rest_framework import serializers, exceptions
from dashboard.models import Performance, Player, Coach, Club, Measurement, ProfilePicture, Unit
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
    url = ProfilePictureSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'is_superuser', 'is_staff', 'is_active', 'username', 'first_name', 'last_name',
                  'email', 'groups', 'date_joined', 'last_login', 'url')


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
        fields = ('id', 'user', 'lab_key', 'gender', 'birthday', 'first_name', 'last_name')


class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ('id', 'user', 'lab_key', 'gender', 'birthday', 'club', 'first_name', 'last_name')


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

