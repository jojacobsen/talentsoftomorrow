from .serializers import CreateDnaHeightSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from django.http import HttpResponse


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class DnaHeightCreateView(generics.CreateAPIView):
    """
    Creates DNA Result by request from DNA Server.
    Return status code.
    * Requires token authentication from admin account.
    """
    authentication_classes = (TokenAuthentication,)

    permission_classes = (IsAdminUser,)
    serializer_class = CreateDnaHeightSerializer
    # Parse JSON
    parser_classes = (JSONParser,)

    def create(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = CreateDnaHeightSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            # Response error message if JSON Format is incorrect
            return JSONResponse(serializer.errors, status=400)
        serializer.save()

        return JSONResponse('DNA result saved in app.', status=201)
