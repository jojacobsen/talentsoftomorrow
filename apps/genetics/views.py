from .models import DnaResult, DnaMeasurement
from .serializers import CreateDnaResultSerializer, DnaResultSerializer, DnaMeasurementSerializer

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


class DnaResultCreateView(generics.CreateAPIView):
    """
    Creates DNA Result.
    Return status code.
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


class DnaResultListView(generics.ListAPIView):
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


class DnaMeasurementListView(generics.ListAPIView):
    serializer_class = DnaMeasurementSerializer
    permission_classes = (IsAuthenticated,)
    queryset = DnaMeasurement.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = DnaMeasurementSerializer(queryset, many=True)
        return JSONResponse(serializer.data)
