from .models import Player, Club, Coach
from .filters import PlayerFilter
from .serializers import NewPlayerSerializer, PlayerSerializer, PlayersSerializer, CurrentPlayerSerializer, \
    CurrentClubSerializer, CurrentCoachSerializer, CoachSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics, exceptions
from rest_framework import filters
from django.http import HttpResponse


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


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


class PlayerDetailView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        group = request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            try:
                queryset = Player.objects.get(pk=pk, club=self.request.user.club, archived=False)
            except Player.DoesNotExist:
                raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        elif 'Coach' in group:
            try:
                queryset = Player.objects.get(pk=pk, club=self.request.user.coach.club, archived=False)
            except Player.DoesNotExist:
                raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        elif 'Player' in group:
            try:
                queryset = Player.objects.get(pk=pk, user=self.request.user, archived=False)
            except Player.DoesNotExist:
                raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        else:
            return JSONResponse('User group not selected.', status=400)

        serializer = PlayerSerializer(queryset)
        return JSONResponse(serializer.data)


class PlayerUpdateView(generics.UpdateAPIView):
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