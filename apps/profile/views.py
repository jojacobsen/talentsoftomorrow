from accounts.models import Player
from .serializers import PlayerProfileSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics, exceptions
from django.http import HttpResponse

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class PlayerProfileView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = PlayerProfileSerializer
    # Parse JSON
    parser_classes = (JSONParser,)

    def get(self, request, pk=None):
        group = self.request.user.groups.values_list('name', flat=True)
        if 'Club' in group:
            queryset = Player.objects.get(pk=pk, club=self.request.user.club, archived=False)
        elif 'Coach' in group:
            queryset = Player.objects.get(pk=pk, club=self.request.user.coach.club, archived=False)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        serializer = PlayerProfileSerializer(queryset)
        return JSONResponse(serializer.data)
