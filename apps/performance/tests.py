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


class TestSerializer(unittest.TestCase):
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

    def test_benchmarkserializer(self):
        from apps.performance.serializers import BenchmarkSerializer
        obj = mock.MagicMock()
        measurements = [mock.MagicMock()]
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
