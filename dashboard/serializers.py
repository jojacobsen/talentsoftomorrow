import uuid
from rest_framework import serializers, exceptions
from dashboard.models import Performance, Player, Coach, Club, Measurement
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'email')


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
        fields = ('id', 'user', 'lab_key', 'gender', 'date_of_birth')


class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    coach = CoachSerializer(read_only=True, many=True)
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ('id', 'user', 'lab_key', 'gender', 'date_of_birth', 'coach', 'club')


class NewPlayersSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coach = CoachSerializer
    club = ClubSerializer

    class Meta:
        model = Player
        fields = ('id', 'user', 'gender', 'date_of_birth', 'coach', 'club')

    def validate(self, data):
        group = self.context['request'].user.groups.values_list('name', flat=True)

        if 'Club' in group:
            if data['club'] != self.context['request'].user.club:
                raise exceptions.PermissionDenied('User can only create players of own club.')
        elif 'Coach' in group:
            if data['club'] != self.context['request'].user.coach.club:
                raise exceptions.PermissionDenied('Coach can only create players of own club.')
            for coach in data['coach']:
                if coach.club != self.context['request'].user.coach.club:
                    raise exceptions.PermissionDenied('Coach can only create players of own club.')

        elif 'Player' in group:
            raise exceptions.PermissionDenied('Players can not create new users.')
        else:
            raise exceptions.PermissionDenied('User group not selected.')

        return data

    def create(self, validated_data):
        coach = validated_data.pop('coach', None)
        user = validated_data.pop('user', None)
        user = User.objects.create_user(username=user['username'],
                                        last_name=user['last_name'],
                                        first_name=user['first_name'])
        validated_data['user'] = user
        validated_data['lab_key'] = str(uuid.uuid5(uuid.NAMESPACE_X500, user.username))
        player = Player.objects.create(**validated_data)
        player.coach = coach
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
            coaches = data['player'].coach.all()
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
