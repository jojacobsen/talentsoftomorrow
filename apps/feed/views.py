import itertools

from .serializers import FeedDashboardSerializer, FeedPlayerSerializer
from accounts.models import Player
from accounts.filters import PlayerFilter
from profile.models import BioAge, PredictedHeight, PHV

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


class FeedDashboardView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    # Parse JSON
    parser_classes = (JSONParser,)

    def get(self, request):
        group = self.request.user.groups.values_list('name', flat=True)
        if 'Club' in group:
            queryset = sorted(list(itertools.chain(
                BioAge.objects.filter(player__club=self.request.user.club),
                PredictedHeight.objects.filter(player__club=self.request.user.club),
                PHV.objects.filter(player__club=self.request.user.club),
            )), key=lambda instance: instance.created, reverse=True)
        elif 'Coach' in group:
            queryset = sorted(list(itertools.chain(
                BioAge.objects.filter(player__club=self.request.user.coach.club),
                PredictedHeight.objects.filter(player__club=self.request.user.coach.club),
                PHV.objects.filter(player__club=self.request.user.coach.club),
            )), key=lambda instance: instance.created, reverse=True)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        serializer = FeedDashboardSerializer(queryset, many=True)
        return JSONResponse(serializer.data)


class FeedPlayerView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    # Parse JSON
    parser_classes = (JSONParser,)

    def get(self, request, pk):
        group = self.request.user.groups.values_list('name', flat=True)
        if 'Club' in group:
            queryset = sorted(list(itertools.chain(
                BioAge.objects.filter(player__id=pk, player__club=self.request.user.club, ),
                PredictedHeight.objects.filter(player__id=pk, player__club=self.request.user.club),
                PHV.objects.filter(player__id=pk, player__club=self.request.user.club),
            )), key=lambda instance: instance.created, reverse=True)
        elif 'Coach' in group:
            queryset = sorted(list(itertools.chain(
                BioAge.objects.filter(player__id=pk, player__club=self.request.user.coach.club),
                PredictedHeight.objects.filter(player__id=pk, player__club=self.request.user.coach.club),
                PHV.objects.filter(player__id=pk, player__club=self.request.user.coach.club),
            )), key=lambda instance: instance.created, reverse=True)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        serializer = FeedDashboardSerializer(queryset, many=True)
        return JSONResponse(serializer.data)
