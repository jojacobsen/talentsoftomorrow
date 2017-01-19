from rest_framework import serializers
from profile.models import PredictedHeight, BioAge, PHV


class FeedDashboardSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        """
        Historic Performance graph.
        :param obj:
        :return:
        """
        if obj.__class__ is BioAge:
            message = 'Bio Age has been determined.'
        if obj.__class__ is PredictedHeight:
            message = 'Predicted Height is ready.'
        if obj.__class__ is PHV:
            message = 'Peak Height Velocity has been calculated.'
        return {
            'player': obj.player.id,
            'created': obj.created,
            'name': ' '.join([obj.player.first_name, obj.player.last_name]),
            'message': message
        }


class FeedPlayerSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        """
        Historic Performance graph.
        :param obj:
        :return:
        """
        if obj.__class__ is BioAge:
            message = 'Bio Age has been determined.'
        if obj.__class__ is PredictedHeight:
            message = 'Predicted Height is ready.'
        if obj.__class__ is PHV:
            message = 'Peak Height Velocity has been calculated.'
        return {
            'created': obj.created,
            'message': message
        }