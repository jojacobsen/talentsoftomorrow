from accounts.models import Player, Club, Coach, Team
from performance.models import Performance
from profile.models import BioAge
from accounts.filters import PlayerFilter
from accounts.serializers import NewPlayerSerializer, PlayerSerializer, PlayersSerializer, CurrentPlayerSerializer, \
    CurrentClubSerializer, CurrentCoachSerializer, CoachSerializer, TeamSerializer, TeamCreateSerializer, ClubCreateSerializer

from django.utils import translation
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics, exceptions
from rest_framework import filters
from django.http import HttpResponse
from password_reset.views import Recover
from password_reset.forms import PasswordRecoveryForm
from rest_framework_jwt.settings import api_settings


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class ClubCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = ClubCreateSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            # Response error message if JSON Format is incorrect
            return JSONResponse(serializer.errors, status=400)
        serializer.save()
        payload = jwt_payload_handler(serializer.instance.user)
        token = jwt_encode_handler(payload)
        return JSONResponse({'token': token})


class PlayerCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewPlayerSerializer
    # Parse JSON
    parser_classes = (JSONParser,)

    def create(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = NewPlayerSerializer(data=data, many=True, context={'request': request})
        if not serializer.is_valid():
            # Response error message if JSON Format is incorrect
            return JSONResponse(serializer.errors, status=400)
        serializer.save()

        return JSONResponse(serializer.data)


class PlayerListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = PlayersSerializer
    filter_class = PlayerFilter

    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Player.objects.filter(club=self.request.user.club, archived=False)
        elif 'Coach' in group:
            queryset = Player.objects.filter(club=self.request.user.coach.club, archived=False)
        elif 'Player' in group:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class PlayerView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlayerSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Player.objects.filter(pk=pk, club=self.request.user.club, archived=False)
        elif 'Coach' in group:
            queryset = Player.objects.filter(pk=pk, club=self.request.user.coach.club, archived=False)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset

    def update(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JSONResponse(serializer.data)


class CoachListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    # Parse JSON
    parser_classes = (JSONParser,)

    def list(self, request):
        group = request.user.groups.values_list('name', flat=True)

        if 'Player' in group:
            queryset = Coach.objects.filter(club=self.request.user.player.club)
        elif 'Coach' in group:
            queryset = Coach.objects.filter(club=self.request.user.coach.club)
        elif 'Club' in group:
            queryset = Coach.objects.filter(club=self.request.user.club)
        else:
            return JSONResponse('User group not selected.', status=400)

        serializer = CoachSerializer(queryset, many=True)
        return JSONResponse(serializer.data)


class UserDetailView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TeamSerializer

    def get(self, request):
        group = request.user.groups.values_list('name', flat=True)

        if 'Player' in group:
            queryset = Player.objects.get(user=self.request.user)
            serializer = CurrentPlayerSerializer(queryset)
        elif 'Coach' in group:
            queryset = Coach.objects.get(user=self.request.user)
            serializer = CurrentCoachSerializer(queryset)
        elif 'Club' in group:
            queryset = Club.objects.get(user=self.request.user)
            serializer = CurrentClubSerializer(queryset)
        else:
            return JSONResponse('User group not selected.', status=400)

        return JSONResponse(serializer.data)


class TeamCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TeamCreateSerializer
    # Parse JSON
    parser_classes = (JSONParser,)


class TeamListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TeamSerializer
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Team.objects.filter(club=self.request.user.club)
        elif 'Coach' in group:
            queryset = Team.objects.filter(club=self.request.user.coach.club)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class TeamView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TeamSerializer
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Team.objects.filter(pk=pk, club=self.request.user.club)
        elif 'Coach' in group:
            queryset = Team.objects.filter(pk=pk, club=self.request.user.coach.club)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class PlayerInviteView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TeamSerializer
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self, pk):
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            try:
                queryset = Player.objects.get(pk=pk, club=self.request.user.club, archived=False)
            except Player.DoesNotExist:
                raise exceptions.NotFound('Player not found.')
        elif 'Coach' in group:
            try:
                queryset = Player.objects.get(pk=pk, club=self.request.user.coach.club, archived=False)
            except Player.DoesNotExist:
                raise exceptions.NotFound('Player not found.')
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset

    def post(self, request, pk):
        player = self.get_queryset(pk)
        if not player.user.email:
            raise exceptions.NotAcceptable('No email address')
        form_data = {
            'username_or_email': player.user.email
        }
        user_language = player.club.language
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language
        invite_form = PasswordRecoveryForm(form_data)
        if invite_form.is_valid():
            r = Recover(request=request,
                        email_template_name='password_reset/invite_email.txt',
                        email_subject_template_name='password_reset/invite_email_subject.txt')
            r.form_valid(invite_form)
            player.invited = timezone.now()
            player.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


class PasswordResetView(APIView):
    permission_classes = (AllowAny,)
    # Parse JSON
    parser_classes = (JSONParser,)

    def post(self, request, email):
        form_data = {
            'username_or_email': email
        }
        recovery_form = PasswordRecoveryForm(form_data)
        if recovery_form.is_valid():
            r = Recover(request=request,
                        email_template_name='password_reset/recovery_email_api.txt',
                        email_subject_template_name='password_reset/recovery_email_api_subject.txt')
            r.form_valid(recovery_form)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

class AccountState(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    # Parse JSON
    parser_classes = (JSONParser,)

    def get(self, request, *args, **kwargs):
        group = self.request.user.groups.values_list('name', flat=True)
        if 'Club' in group:
            club = self.request.user.club
        elif 'Coach' in group:
            club = self.request.user.coach.club
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        has_talents = Player.objects.filter(club=club, archived=False).exists()
        has_test = Performance.objects.filter(player__club=club, player__archived=False).exists()
        has_bioage = BioAge.objects.filter(player__club=club, player__archived=False).exists()
        return JSONResponse({
            "accountState": {
                "hasTalents": has_talents,
                "hasTestData": has_test,
                "hasBioAge": has_bioage,
            }
        })

