from rest_framework import serializers, exceptions
from .models import DnaResult, DnaMeasurement
from accounts.models import Player


class DnaMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DnaMeasurement


class DnaResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DnaResult


class CreateDnaResultSerializer(serializers.ModelSerializer):
    player = serializers.CharField()
    dna_measurement = serializers.CharField()

    class Meta:
        model = DnaResult
        fields = ('date', 'value', 'original_filename', 'player', 'dna_measurement', 'meta')

    def validate(self, data):
        try:
            player = Player.objects.get(lab_key=data['player'])
        except Player.DoesNotExist:
            raise exceptions.NotFound('Player not found.')

        try:
            dna_measurement = DnaMeasurement.objects.get(slug_name=data['dna_measurement'])
        except DnaMeasurement.DoesNotExist:
            raise exceptions.NotFound('Player not found.')

        data['player'] = player
        data['dna_measurement'] = dna_measurement
        return data

    def create(self, validated_data):
        dna_result = DnaResult.objects.create(**validated_data)
        return dna_result
