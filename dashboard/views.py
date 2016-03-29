from dashboard.models import Performance, Player
from dashboard.serializers import PerformanceSerializer, PlayersSerializer, PlayerSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics, exceptions
from django.views import generic
from django.http import HttpResponse


class IndexView(generic.TemplateView):
    template_name = 'dashboard/index.html'


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class PlayerListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        group = request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Player.objects.filter(club__user=self.request.user)
        elif 'Coach' in group:
            queryset = Player.objects.filter(coach__user=self.request.user)
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
                queryset = Player.objects.get(pk=pk, club__user=self.request.user)
            except Player.DoesNotExist:
                raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        elif 'Coach' in group:
            try:
                queryset = Player.objects.get(pk=pk, coach__user=self.request.user)
            except Player.DoesNotExist:
                raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        elif 'Player' in group:
            try:
                queryset = Player.objects.get(pk=pk, user=self.request.user)
            except Player.DoesNotExist:
                raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        else:
            return JSONResponse('User group not selected.', status=400)

        serializer = PlayerSerializer(queryset)
        return JSONResponse(serializer.data)


class PerformanceListView(generics.ListCreateAPIView):
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

        return HttpResponse(status=201)

    def list(self, request):
        group = request.user.groups.values_list('name', flat=True)

        if 'Player' in group:
            queryset = Performance.objects.filter(player__user=self.request.user)
        elif 'Coach' in group:
            queryset = Performance.objects.filter(player__coach__user=self.request.user)
        elif 'Club' in group:
            queryset = Performance.objects.filter(player__club__user=self.request.user)
        else:
            return JSONResponse('User group not selected.', status=400)

        serializer = PerformanceSerializer(queryset, many=True)
        return JSONResponse(serializer.data)

