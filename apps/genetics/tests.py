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


class TestSerializer(unittest.TestCase):
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
