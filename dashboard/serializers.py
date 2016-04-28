import uuid
import random
from rest_framework import serializers, exceptions
from dashboard.models import Performance, Player, Coach, Club, Measurement
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


class CurrentUserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ('is_superuser', 'is_staff', 'is_active', 'username', 'first_name', 'last_name',
                  'email', 'groups', 'date_joined', 'last_login')


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
        fields = ('id', 'user', 'lab_key', 'gender', 'birthday')


class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    coaches = CoachSerializer(read_only=True, many=True)
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ('id', 'user', 'lab_key', 'gender', 'birthday', 'coaches', 'club')


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
        fields = ('id', 'user', 'club', 'gender', 'birthday')


class NewPlayersSerializer(serializers.ModelSerializer):
    user = NewUserSerializer()
    coaches = CoachSerializer
    club = ClubSerializer

    class Meta:
        model = Player
        fields = ('user', 'gender', 'birthday', 'coaches')

    def validate(self, data):
        group = self.context['request'].user.groups.values_list('name', flat=True)

        if 'Club' in group:
            return data
        elif 'Coach' in group:
            for coach in data['coaches']:
                if coach.club != self.context['request'].user.coach.club:
                    raise exceptions.PermissionDenied('Coach can only create players for coaches of own club.')
                else:
                    return data
        elif 'Player' in group:
            raise exceptions.PermissionDenied('Players can not create new users.')
        else:
            raise exceptions.PermissionDenied('User group not selected.')

    def create(self, validated_data):
        coaches = validated_data.pop('coaches', None)

        # Check the group of the current user
        group = self.context['request'].user.groups.values_list('name', flat=True)
        if 'Club' in group:
            validated_data['club'] = self.context['request'].user.club
        elif 'Coach' in group:
            validated_data['club'] = self.context['request'].user.coach.club

        # Create the user for the player
        user = validated_data.pop('user', None)
        username = create_username(last_name=user['last_name'], first_name=user['first_name'])
        user = User.objects.create_user(username=username,
                                        last_name=user['last_name'],
                                        first_name=user['first_name'])
        # Add the group
        player_group = Group.objects.get(name='Player')
        user.groups.add(player_group)
        validated_data['user'] = user
        validated_data['lab_key'] = str(uuid.uuid5(uuid.NAMESPACE_X500, user.username))

        # Create the player
        player = Player.objects.create(**validated_data)
        player.coaches = coaches
        return player


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance

    def validate(self, data):
        group = self.context['request'].user.groups.values_list('name', flat=True)

        if 'Club' in group:
            if data['player'].club.user != self.context['request'].user:
                raise exceptions.PermissionDenied('Club has no permission to access performance data of player.')
        elif 'Coach' in group:
            coaches = data['player'].coaches.all()
            if self.context['request'].user.coach not in coaches:
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


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement

