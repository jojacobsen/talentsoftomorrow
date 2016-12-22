from .serializers import PerformanceAnalyseSerializer, PerformanceHistoricSerializer, PerformanceToBioAgeSerializer, \
    HeightEstimationSerializer
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
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class PerformanceAnaylseListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = PerformanceAnalyseSerializer
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


class PerformanceHistoricListView(generics.ListAPIView):
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


class PerformanceToBioAgeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = PerformanceToBioAgeSerializer
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


class HeightEstimationListView(generics.ListAPIView):
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
