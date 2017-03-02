from unittest import mock
import unittest


class TestViews(unittest.TestCase):
    @mock.patch('apps.performance.views.JSONRenderer')
    def test_jsonresponse(self, mock_jsonrenderer):
        from apps.performance.views import JSONResponse
        content = mock.MagicMock()
        mock_jsonrenderer.return_value.render.return_value = content
        data = mock.MagicMock()
        response = JSONResponse(data)
        self.assertEquals(response.status_code, 200)

    @mock.patch('apps.performance.views.JSONResponse')
    @mock.patch('apps.performance.views.JSONParser')
    @mock.patch('apps.performance.views.PerformanceSerializer')
    def test_performancecreateview(self, mock_performanceserializer, mock_jsonparser, mock_jsonrsponse):
        from apps.performance.views import PerformanceCreateView
        performance = PerformanceCreateView()
        json_response = mock.MagicMock()
        mock_jsonrsponse.return_value = json_response
        mock_performanceserializer.return_value = mock.MagicMock()
        data = mock.MagicMock()
        mock_jsonparser.return_value.parse.return_value = data
        request = mock.MagicMock()
        response = performance.create(request, None)
        self.assertEquals(response, json_response)

    @mock.patch('apps.performance.views.Performance')
    def test_performancelistview(self, mock_performance):
        from apps.performance.views import PerformanceListView
        request = mock.MagicMock()
        queryset = mock.MagicMock()
        mock_performance.objects.filter.return_value.order_by.return_value = queryset
        request.user.groups.values_list.return_value = 'Club'
        performances = PerformanceListView(request=request)
        return_queryset = performances.get_queryset()
        self.assertEquals(return_queryset, queryset)
        request.user.groups.values_list.return_value = 'Coach'
        return_queryset = performances.get_queryset()
        self.assertEquals(return_queryset, queryset)

    @mock.patch('apps.performance.views.JSONResponse')
    @mock.patch('apps.performance.views.PerformanceSerializer')
    @mock.patch('apps.performance.views.Performance')
    def test_performancedetailview(self, mock_performance, mock_performanceserializer, mock_jsonrsponse):
        from apps.performance.views import PerformanceDetailView
        request = mock.MagicMock()
        performance = mock.MagicMock()
        mock_performance.objects.get.return_value = performance
        mock_performanceserializer.return_value = mock.MagicMock()
        response = mock.MagicMock()
        mock_jsonrsponse.return_value = response
        request.user.groups.values_list.return_value = 'Club'
        p = PerformanceDetailView(request=request)
        response_test = p.get(request)
        self.assertEquals(response_test, response)
        request.user.groups.values_list.return_value = 'Coach'
        response_test = p.get(request)
        self.assertEquals(response_test, response)

    @mock.patch('apps.performance.views.Performance')
    def test_performanceupdateview_queryset(self, mock_performance):
        from apps.performance.views import PerformanceUpdateView
        request = mock.MagicMock()
        queryset = mock.MagicMock()
        mock_performance.objects.filter.return_value = queryset
        request.user.groups.values_list.return_value = 'Club'
        kwargs = mock.MagicMock()
        performances = PerformanceUpdateView(request=request, kwargs=kwargs)
        return_queryset = performances.get_queryset()
        self.assertEquals(return_queryset, queryset)
        request.user.groups.values_list.return_value = 'Coach'
        return_queryset = performances.get_queryset()
        self.assertEquals(return_queryset, queryset)

    @mock.patch('apps.performance.views.Performance')
    def test_performancedeleteview_queryset(self, mock_performance):
        from apps.performance.views import PerformanceDeleteView
        request = mock.MagicMock()
        queryset = mock.MagicMock()
        mock_performance.objects.filter.return_value = queryset
        request.user.groups.values_list.return_value = 'Club'
        kwargs = mock.MagicMock()
        performances = PerformanceDeleteView(request=request, kwargs=kwargs)
        return_queryset = performances.get_queryset()
        self.assertEquals(return_queryset, queryset)
        request.user.groups.values_list.return_value = 'Coach'
        return_queryset = performances.get_queryset()
        self.assertEquals(return_queryset, queryset)

    def test_measurementlistview_queryset(self):
        from apps.performance.views import MeasurementListView
        request = mock.MagicMock()
        queryset = mock.MagicMock()
        request.user.club.measurements.filter.return_value = queryset
        request.user.groups.values_list.return_value = 'Club'
        m = MeasurementListView(request=request)
        return_queryset = m.get_queryset()
        self.assertEquals(return_queryset, queryset)
        request.user.coach.club.measurements.filter.return_value = queryset
        request.user.groups.values_list.return_value = 'Coach'
        return_queryset = m.get_queryset()
        self.assertEquals(return_queryset, queryset)
        request.user.player.club.measurements.filter.return_value = queryset
        request.user.groups.values_list.return_value = 'Player'
        return_queryset = m.get_queryset()
        self.assertEquals(return_queryset, queryset)

    @mock.patch('apps.performance.views.Player')
    def test_benchmarklistview_queryset(self, mock_player):
        from apps.performance.views import BenchmarkListView
        request = mock.MagicMock()
        queryset = mock.MagicMock()
        mock_player.objects.filter.return_value = queryset
        request.user.groups.values_list.return_value = 'Club'
        performances = BenchmarkListView(request=request)
        return_queryset = performances.get_queryset()
        self.assertEquals(return_queryset, queryset)
        request.user.groups.values_list.return_value = 'Coach'
        return_queryset = performances.get_queryset()
        self.assertEquals(return_queryset, queryset)


class TestSerializers(unittest.TestCase):
    def test_performanceplayerserializer(self):
        from apps.performance.serializers import PerformancePlayerSerializer
        obj = mock.MagicMock()
        measurements = [mock.MagicMock()]
        obj.club.measurements.filter.return_value = measurements
        measurement = mock.MagicMock(category='test')
        performances = [mock.MagicMock(value=5, measurement=measurement),
                        mock.MagicMock(value=6, measurement=measurement)]
        obj.performance_set.filter.return_value.order_by.return_value = performances
        view = mock.MagicMock()
        serializer = PerformancePlayerSerializer(context={'view': view})
        validated_data = serializer.to_representation(obj)
        self.assertEquals(validated_data['test'][0]['value'], 5)
        self.assertEquals(validated_data['test'][0]['progress'], 'up')
        self.assertEquals(validated_data['benchmark_bio_ave'], 1.0)
        self.assertEquals(validated_data['benchmark_chrono_ave'], 1.0)

    @mock.patch('apps.performance.serializers.round')
    def test_benchmarkserializer(self, mock_round):
        from apps.performance.serializers import BenchmarkSerializer
        obj = mock.MagicMock()
        obj.first_name = 'John'
        obj.last_name = 'Doe'
        mock_round.return_value = 15.0
        measurements = [mock.MagicMock()]
        bio_age = 16
        bio_age_method = 'pre'
        obj.bioage_set.values_list.return_value.latest.return_value = [bio_age, bio_age_method]
        obj.club.measurements.filter.return_value = measurements
        measurement = mock.MagicMock(category='test')
        performances = mock.MagicMock(value=5, measurement=measurement)
        obj.performance_set.filter.return_value.latest.return_value = performances
        view = mock.MagicMock()
        serializer = BenchmarkSerializer(context={'view': view})
        validated_data = serializer.to_representation(obj)
        self.assertEquals(validated_data['player'], obj.id)

    def test_performanceserializer(self):
        from apps.performance.serializers import PerformanceSerializer
        data = dict()
        data['value'] = 5
        club = mock.MagicMock()
        request = mock.MagicMock()
        data['player'] = mock.MagicMock(club=club)
        data['measurement'] = mock.MagicMock()
        data['measurement'].lower_limit = 2
        data['measurement'].upper_limit = 10
        request.user.club = club
        request.user.groups.values_list.return_value = 'Club'
        serializer = PerformanceSerializer(context={'request': request})
        validated_data = serializer.validate(data)
        self.assertEquals(validated_data['player'].club, club)
