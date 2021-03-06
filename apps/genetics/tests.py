from unittest import mock
import unittest


class TestSignals(unittest.TestCase):
    @mock.patch('apps.genetics.signals.handlers.PredictedHeight')
    def test_post_khamis_roche_handler(self, mock_predictedheight):
        from apps.genetics.signals.handlers import post_dna_height_handler
        sender = mock.MagicMock()
        instance = mock.MagicMock()
        mock_predictedheight.objects.create.return_value = mock.MagicMock()
        post_dna_height_handler(sender, instance, created=True)
        mock_predictedheight.objects.create.assert_called_with(player=instance.player,
                                                               date=instance.date,
                                                               predicted_height=instance.predicted_height,
                                                               method='dna',
                                                               khamis_roche=None,
                                                               dna_height=instance)
        post_dna_height_handler(sender, instance, created=False)
        instance.player.predictedheight_set.filter.assert_called_with(dna_height=instance)


class TestSerializers(unittest.TestCase):
    @mock.patch('apps.genetics.serializers.Player')
    def test_validate_dnaheightserializer(self, mock_player):
        from apps.genetics.serializers import CreateDnaHeightSerializer
        data = mock.MagicMock()
        request = mock.MagicMock()
        player = mock.MagicMock()
        mock_player.objects.get.return_value = player
        serializer = CreateDnaHeightSerializer(context={'request': request})
        validated_data = serializer.validate(data)
        validated_data.assert_has_calls(player)


class TestViews(unittest.TestCase):
    @mock.patch('apps.genetics.views.JSONRenderer')
    def test_jsonresponse(self, mock_jsonrenderer):
        from apps.genetics.views import JSONResponse
        content = mock.MagicMock()
        mock_jsonrenderer.return_value.render.return_value = content
        data = mock.MagicMock()
        response = JSONResponse(data)
        self.assertEquals(response.status_code, 200)

    @mock.patch('apps.genetics.views.JSONResponse')
    @mock.patch('apps.genetics.views.JSONParser')
    @mock.patch('apps.genetics.views.CreateDnaHeightSerializer')
    def test_dnaheightcreate(self, mock_dnaheightserializer, mock_jsonparser, mock_jsonrsponse):
        from apps.genetics.views import DnaHeightCreateView
        dna_height = DnaHeightCreateView()
        json_response = mock.MagicMock()
        mock_jsonrsponse.return_value = json_response
        mock_dnaheightserializer.return_value = mock.MagicMock()
        data = mock.MagicMock
        mock_jsonparser.return_value.parse.return_value = data
        request = mock.MagicMock()
        response = dna_height.create(request, None)
        self.assertEquals(response, json_response)
