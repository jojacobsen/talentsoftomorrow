from .serializers import PerformanceHistoricSerializer, PerformanceBioAgeSerializer, HeightEstimationSerializer, \
    PerformanceGraphSerializer
from accounts.models import Player
from accounts.filters import PlayerFilter

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
        data = filter(None, data)
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class PerformanceHistoricGraphView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = PerformanceHistoricSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PlayerFilter
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)
        if 'Club' in group:
            queryset = Player.objects.filter(club=self.request.user.club, archived=False)
        elif 'Coach' in group:
            queryset = Player.objects.filter(club=self.request.user.coach.club, archived=False)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset

    def get(self, request, pk, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PerformanceHistoricSerializer(queryset, many=True, context={'pk': pk})
        return JSONResponse(serializer.data)


class PerformanceBioAgeGraphView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PlayerFilter
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)
        if 'Club' in group:
            queryset = Player.objects.filter(club=self.request.user.club, archived=False)
        elif 'Coach' in group:
            queryset = Player.objects.filter(club=self.request.user.coach.club, archived=False)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset

    def get(self, request, pk, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PerformanceBioAgeSerializer(queryset, many=True, context={'pk': pk})
        return JSONResponse(serializer.data)


class PerformanceGraphView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PlayerFilter
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)
        if 'Club' in group:
            queryset = Player.objects.filter(club=self.request.user.club, archived=False)
        elif 'Coach' in group:
            queryset = Player.objects.filter(club=self.request.user.coach.club, archived=False)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset

    def get(self, request, pk, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PerformanceGraphSerializer(queryset, many=True, context={'pk': pk})
        return JSONResponse(serializer.data)


class HeightEstimationGraphView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = HeightEstimationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PlayerFilter
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)
        if 'Club' in group:
            queryset = Player.objects.filter(club=self.request.user.club, archived=False)
        elif 'Coach' in group:
            queryset = Player.objects.filter(club=self.request.user.coach.club, archived=False)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = HeightEstimationSerializer(queryset, many=True)
        return JSONResponse(serializer.data)
