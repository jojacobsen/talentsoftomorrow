from dashboard.models import Performance, Player, DnaMeasurement, Coach, Club, DnaResult
from dashboard.serializers import PerformanceSerializer, PlayersSerializer, \
    PlayerSerializer, MeasurementSerializer, NewPlayersSerializer, CoachSerializer, CurrentClubSerializer, \
    CurrentCoachSerializer, CurrentPlayerSerializer, DnaResultSerializer, DnaMeasurementSerializer, \
    CreateDnaResultSerializer, PerformanceAnalyse, PerformanceAnalyseSerializer, PerformancesHistoricSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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


class PlayersCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewPlayersSerializer
    # Parse JSON
    parser_classes = (JSONParser,)

    def create(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = NewPlayersSerializer(data=data, many=True, context={'request': request})
        if not serializer.is_valid():
            # Response error message if JSON Format is incorrect
            return JSONResponse(serializer.errors, status=400)
        serializer.save()

        return JSONResponse(serializer.data)


class PlayersListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    # Parse JSON
    parser_classes = (JSONParser,)

    def list(self, request):
        group = request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Player.objects.filter(club=self.request.user.club, archived=False)
        elif 'Coach' in group:
            queryset = Player.objects.filter(club=self.request.user.coach.club, archived=False)
        elif 'Player' in group:
            return JSONResponse('Players can not see players list.', status=403)
        else:
            return JSONResponse('User group not selected.', status=400)

        serializer = PlayersSerializer(queryset, many=True, context={'request': request})
        return JSONResponse(serializer.data)


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
            queryset = Player.objects.filter(pk=pk, club=self.request.user.club)
        elif 'Coach' in group:
            queryset = Player.objects.filter(pk=pk, club=self.request.user.coach.club)
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


class PerformancesCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    # Parse JSON
    parser_classes = (JSONParser,)

    def create(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = PerformanceSerializer(data=data, many=True, context={'request': request})
        if not serializer.is_valid():
            # Response error message if JSON Format is incorrect
            return JSONResponse(serializer.errors, status=400)
        serializer.save()

        return JSONResponse(serializer.data)


class PerformancesListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PerformanceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('player', 'measurement')
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Performance.objects.filter(player__club=self.request.user.club)
        elif 'Coach' in group:
            queryset = Performance.objects.filter(player__club=self.request.user.coach.club)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class PerformanceDetailView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        group = request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            try:
                queryset = Performance.objects.get(pk=pk, player__club=self.request.user.club)
            except Performance.DoesNotExist:
                raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        elif 'Coach' in group:
            try:
                queryset = Performance.objects.get(pk=pk, player__club=self.request.user.coach.club)
            except Performance.DoesNotExist:
                raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        elif 'Player' in group:
            try:
                queryset = Performance.objects.get(pk=pk, player__user=self.request.user)
            except Performance.DoesNotExist:
                raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        else:
            return JSONResponse('User group not selected.', status=400)

        serializer = PerformanceSerializer(queryset)

        return JSONResponse(serializer.data)


class PerformanceUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PerformanceSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Performance.objects.filter(pk=pk, player__club=self.request.user.club)
        elif 'Coach' in group:
            queryset = Performance.objects.filter(pk=pk, player__club=self.request.user.coach.club)
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


class PerformanceDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PerformanceSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Performance.objects.filter(pk=pk, player__club=self.request.user.club)
        elif 'Coach' in group:
            queryset = Performance.objects.filter(pk=pk, player__club=self.request.user.coach.club)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class MeasurementsListView(generics.ListAPIView):
    serializer_class = MeasurementSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = self.request.user.club.measurements.filter()
        elif 'Coach' in group:
            queryset = self.request.user.coach.club.measurements.filter()
        elif 'Player' in group:
            queryset = self.request.user.player.club.measurements.filter()
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = MeasurementSerializer(queryset, many=True)
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


class DnaResultCreateView(generics.CreateAPIView):
    """
    Creates DNA Result.
    Raturn status code.
    * Requires token authentication from admin account.
    """
    authentication_classes = (TokenAuthentication,)

    permission_classes = (IsAdminUser,)
    serializer_class = CreateDnaResultSerializer
    # Parse JSON
    parser_classes = (JSONParser,)

    def create(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = CreateDnaResultSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            # Response error message if JSON Format is incorrect
            return JSONResponse(serializer.errors, status=400)
        serializer.save()

        return JSONResponse('DNA result saved in app.', status=201)


class DnaResultsListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DnaResultSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('player', 'dna_measurement')
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = DnaResult.objects.filter(player__club=self.request.user.club)
        elif 'Coach' in group:
            queryset = DnaResult.objects.filter(player__club=self.request.user.coach.club)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class DnaMeasurementsListView(generics.ListAPIView):
    serializer_class = DnaMeasurementSerializer
    permission_classes = (IsAuthenticated,)
    queryset = DnaMeasurement.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = DnaMeasurementSerializer(queryset, many=True)
        return JSONResponse(serializer.data)


class PerformanceAnaylseListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    # Parse JSON
    parser_classes = (JSONParser,)

    def list(self, request):
        group = request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Performance.objects.filter(player__club=self.request.user.club)
        elif 'Coach' in group:
            queryset = PerformanceAnalyse.objects.filter(player__club=self.request.user.coach.club)
        elif 'Player' in group:
            return JSONResponse('Players can not see players list.', status=403)
        else:
            return JSONResponse('User group not selected.', status=400)
        serializer = PerformanceAnalyseSerializer(queryset, many=True, context={'request': request})
        return JSONResponse(serializer.data)


class PerformancesHistoricListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('player', 'measurement')
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self, pk):
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Performance.objects.filter(measurement__id=pk, player__club=self.request.user.club)
        elif 'Coach' in group:
            queryset = Performance.objects.filter(measurement__id=pk, player__club=self.request.user.coach.club)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset

    def list(self, request, pk):
        queryset = self.get_queryset(pk=pk)
        serializer = PerformancesHistoricSerializer(queryset)
        return JSONResponse(serializer.data)
