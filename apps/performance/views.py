from .serializers import PerformanceSerializer, MeasurementSerializer
from .models import Performance
from .filters import PerformanceFilter

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


class PerformanceCreateView(generics.CreateAPIView):
    """
    Creates Performance object.
    """
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


class PerformanceListView(generics.ListAPIView):
    """
    List performances of players in club.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PerformanceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PerformanceFilter
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Performance.objects.filter(player__club=self.request.user.club).order_by('-created')
        elif 'Coach' in group:
            queryset = Performance.objects.filter(player__club=self.request.user.coach.club).order_by('-created')
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class PerformanceDetailView(generics.GenericAPIView):
    """
    Detailed performance view.
    """
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
    """
    Updates Performance object.
    """
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
    """
    Deletes Performance object.
    """
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


class MeasurementListView(generics.ListAPIView):
    """
    List Measurements of clubs.
    """
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


