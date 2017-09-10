from performance.serializers import PerformanceSerializer, MeasurementSerializer, \
    PerformancePlayerSerializer, BenchmarkSerializer
from performance.models import Performance
from performance.filters import PerformanceFilter
from accounts.models import Player
from accounts.filters import PlayerFilter
from profile.serializers import HeightSerializer, WeightSerializer, SittingHeightSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework import generics, exceptions
from rest_framework import filters
from django.http import HttpResponse
from rest_framework.views import APIView
import django_excel
from performance.excel import create_excel_template


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


class PerformanceView(generics.RetrieveUpdateDestroyAPIView):
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


class PerformancePlayerView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = PerformancePlayerSerializer
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

        serializer = PerformancePlayerSerializer(queryset)
        return JSONResponse(serializer.data)


class BenchmarkListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = BenchmarkSerializer
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


class PerformanceImportView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        try:
            height_data = request.FILES['file'].get_records(sheet_name='Height', name_columns_by_row=0)
        except ValueError:
            height_data = None

        if height_data:
            height_serializer = HeightSerializer(data=height_data, many=True, context={'request': request})
            if not height_serializer.is_valid():
                # Response error message if JSON Format is incorrect
                return JSONResponse(height_serializer.errors, status=400)

        try:
            weight_data = request.FILES['file'].get_records(sheet_name='Weight', name_columns_by_row=0)
        except ValueError:
            weight_data = None

        if weight_data:
            weight_serializer = WeightSerializer(data=weight_data, many=True, context={'request': request})
            if not weight_serializer.is_valid():
                # Response error message if JSON Format is incorrect
                return JSONResponse(weight_serializer.errors, status=400)

        try:
            sitting_height_data = request.FILES['file'].get_records(sheet_name='Sitting Height', name_columns_by_row=0)
        except ValueError:
            sitting_height_data = None

        if sitting_height_data:
            sitting_height_serializer = SittingHeightSerializer(
                data=sitting_height_data,
                many=True, context={'request': request})
            if not sitting_height_serializer.is_valid():
                # Response error message if JSON Format is incorrect
                return JSONResponse(sitting_height_serializer.errors, status=400)

        try:
            performance_data = request.FILES['file'].get_records(sheet_name='Performance', name_columns_by_row=0)
        except ValueError:
            performance_data = None

        if performance_data:
            performance_serializer = PerformanceSerializer(data=performance_data, many=True, context={'request': request})
            if not performance_serializer.is_valid():
                # Response error message if JSON Format is incorrect
                return JSONResponse(performance_serializer.errors, status=400)

        if height_data:
            height_serializer.save()
        if weight_data:
            weight_serializer.save()
        if sitting_height_data:
            sitting_height_serializer.save()
        if performance_data:
            performance_serializer.save()

        return JSONResponse('Import successful', status=204)


class TemplateDownloadView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        book = create_excel_template(request)
        return django_excel.make_response(book, "xlsx", file_name="ToT_template")
