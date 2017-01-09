from unittest import mock
import unittest
import decimal


class TestViews(unittest.TestCase):
    @mock.patch('apps.graphs.views.JSONRenderer')
    def test_jsonresponse(self, mock_jsonrenderer):
        from apps.graphs.views import JSONResponse
        content = mock.MagicMock()
        mock_jsonrenderer.return_value.render.return_value = content
        data = mock.MagicMock()
        response = JSONResponse(data)
        self.assertEquals(response.status_code, 200)


class TestSerializer(unittest.TestCase):
    def test_performancehistoricserializer(self):
        from apps.graphs.serializers import PerformanceHistoricSerializer
        obj = mock.MagicMock()
        performances = [mock.MagicMock()]
        obj.performance_set.filter.return_value = performances
        view = mock.MagicMock()
        serializer = PerformanceHistoricSerializer(context={'view': view})
        validated_data = serializer.to_representation(obj)
        self.assertEquals(validated_data['player'], obj.id)

    def test_performancebioageserializer(self):
        from apps.graphs.serializers import PerformanceBioAgeSerializer
        obj = mock.MagicMock()
        performances_value = decimal.Decimal(4)
        obj.performance_set.filter.return_value.values_list.return_value.latest.return_value = performances_value
        bio_age = decimal.Decimal(15)
        obj.bioage_set.values_list.return_value.latest.return_value = bio_age
        view = mock.MagicMock()
        serializer = PerformanceBioAgeSerializer(context={'view': view})
        validated_data = serializer.to_representation(obj)
        self.assertEquals(validated_data['data'][0]['x'], bio_age)
        self.assertEquals(validated_data['data'][0]['y'], performances_value)

    @mock.patch('apps.graphs.serializers.round')
    def test_performancegraphserializer(self, mock_round):
        from apps.graphs.serializers import PerformanceGraphSerializer
        obj = mock.MagicMock()
        performances = mock.MagicMock()
        date = mock.MagicMock()
        age = 14.5
        mock_round.return_value = age
        obj.performance_set.filter.return_value.values_list.return_value.latest.return_value = [performances, date]
        view = mock.MagicMock()
        serializer = PerformanceGraphSerializer(context={'view': view})
        validated_data = serializer.to_representation(obj)
        self.assertEquals(validated_data['player'], obj.id)
        self.assertEquals(validated_data['data'][0]['x'], age)

    @mock.patch('apps.graphs.serializers.round')
    def test_heightestimationserializer(self, mock_round):
        from apps.graphs.serializers import HeightEstimationSerializer
        obj = mock.MagicMock()
        height = mock.MagicMock()
        age = 14.5
        mock_round.return_value = age
        current_height = 4.0
        height_unit = 's'
        prediction = mock.MagicMock()
        obj.predictedheight_set.filter.return_value.latest.return_value = prediction
        predicted_height = 185
        prediction.value_club_unit.return_value = [predicted_height, height_unit]
        obj.height_set.filter.return_value.latest.return_value = height
        height.value_club_unit.return_value = [current_height, height_unit]
        view = mock.MagicMock()
        serializer = HeightEstimationSerializer(context={'view': view})
        validated_data = serializer.to_representation(obj)
        self.assertEquals(validated_data['player'], obj.id)
        self.assertEquals(validated_data['data'][0]['x'], age)
        self.assertEquals(validated_data['data'][0]['y'], current_height)
