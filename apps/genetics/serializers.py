from rest_framework import serializers, exceptions
from genetics.models import DnaHeight
from accounts.models import Player
from measurement.measures import Distance


class DnaHeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = DnaHeight
        fields = '__all__'


class CreateDnaHeightSerializer(serializers.ModelSerializer):
    player = serializers.CharField()

    class Meta:
        model = DnaHeight
        fields = ('date', 'predicted_height', 'original_filename', 'player', 'meta')

    def validate(self, data):
        try:
            player = Player.objects.get(lab_key=data['player'])
        except Player.DoesNotExist:
            raise exceptions.NotFound('Player not found.')

        data['player'] = player
        data['predicted_height'] = Distance(cm=data['predicted_height'])
        return data
