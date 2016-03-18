from dashboard.serializers import PerformanceSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
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


class PerformanceList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    # Parse JSON
    parser_classes = (JSONParser,)

    def create(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = PerformanceSerializer(data=data, many=True)
        if not serializer.is_valid():
            # Response error message if JSON Format is incorrect
            return JSONResponse(serializer.errors, status=400)
        serializer.save()

        return HttpResponse(status=201)

