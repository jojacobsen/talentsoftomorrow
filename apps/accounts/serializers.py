from accounts.models import ProfilePicture, Club, Coach, Player, Team
from rest_framework import serializers, exceptions
from django.contrib.auth.models import User, Group
from .utils import create_username, lab_key_generator
from collections import OrderedDict
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = '__all__'


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
        fields = '__all__'


class CoachSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Coach
        fields = ('id', 'club', 'user')


class PlayersSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ('id', 'username', 'email', 'lab_key', 'gender', 'birthday', 'first_name',
                  'last_name', 'active', 'archived', 'invited')

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email


class PlayerSerializer(serializers.ModelSerializer):
    club = ClubSerializer(read_only=True)
    email = serializers.EmailField()

    class Meta:
        model = Player
        fields = ('id', 'lab_key', 'gender', 'birthday', 'club', 'first_name', 'last_name', 'active',
                  'archived', 'email')

    def to_representation(self, instance):
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                if field.field_name == 'email':
                    attribute = field.get_attribute(instance.user)
                else:
                    attribute = field.get_attribute(instance)
            except SkipField:
                continue
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'email':
                setattr(instance.user, attr, value)
                instance.user.save()
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class CurrentClubSerializer(serializers.ModelSerializer):
    user = CurrentUserSerializer(read_only=True)

    class Meta:
        model = Club
        fields = '__all__'


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


class ClubCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=30, min_length=5, write_only=True, required=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    class Meta:
        model = Club
        fields = ('username', 'password', 'name', 'email', 'first_name', 'last_name', 'gender', 'measurement_system')

    def create(self, validated_data):
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        password = validated_data.pop('password')
        if User.objects.filter(username=username).exists():
            raise exceptions.NotAcceptable("Username exists")
        if User.objects.filter(email=email).exists():
            raise exceptions.NotAcceptable("Email address exists")

        user = User.objects.create_user(
            username=username, password=password,
            email=email, first_name=first_name,
            last_name=last_name
        )

        validated_data['user'] = user
        # Add the group
        club_group = Group.objects.get(name='Club')
        user.groups.add(club_group)

        # Create club
        club = Club.objects.create(**validated_data)
        return club


class NewPlayerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=None, min_length=5, allow_blank=True, write_only=True, required=False)

    class Meta:
        model = Player
        fields = ('birthday', 'first_name', 'last_name', 'gender', 'email', 'active', 'archived')

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
        if validated_data.get('email'):
            email = validated_data.pop('email')
        else:
            email = None

        # Create the user for the player
        username = create_username(last_name=validated_data['last_name'], first_name=validated_data['first_name'])
        user = User.objects.create_user(username=username, email=email)
        # Add the group
        player_group = Group.objects.get(name='Player')
        user.groups.add(player_group)
        validated_data['user'] = user
        validated_data['lab_key'] = lab_key_generator()

        # Create the player
        player = Player.objects.create(**validated_data)
        return player


class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        exclude = ('club',)

    def create(self, validated_data):
        # Check the group of the current user
        group = self.context['request'].user.groups.values_list('name', flat=True)
        if 'Club' in group:
            validated_data['club'] = self.context['request'].user.club
        elif 'Coach' in group:
            validated_data['club'] = self.context['request'].user.coach.club

        # Create the team
        team = Team.objects.create(**validated_data)
        return team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
