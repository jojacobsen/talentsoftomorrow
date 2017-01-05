import datetime
from rest_framework import serializers
from profile.models import Height, Weight, PredictedHeight, BioAge


class PlayerProfileSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        measurement_system = obj.club.measurement_system
        try:
            current_height, height_date = obj.height_set.values_list('height', 'date').latest('date')
            # Uses the date when height was recorded
            current_age = round((height_date - obj.birthday).days / 365.25, 1)
            if measurement_system == 'SI':
                current_height = current_height.cm
                height_unit = 'cm'
            elif measurement_system == 'Imp':
                current_height = current_height.inch
                height_unit = 'inch'
        except Height.DoesNotExist:
            current_height = None
            current_age = round((datetime.date.today() - obj.birthday).days / 365.25, 1)

        # Get latest weight record
        try:
            current_weight = obj.weight_set.values_list('weight', flat=True).latest('date')
            if measurement_system == 'SI':
                current_weight = current_weight.kg
                weight_unit = 'kg'
            elif measurement_system == 'Imp':
                current_weight = current_weight.lb
                weight_unit = 'lb'

        except Weight.DoesNotExist:
            current_weight = None
            weight_unit = None

        try:
            # DNA result always highest prio
            predicted_height, prediction_method = obj.predictedheight_set.filter(
                method='dna'
            ).values_list(
                'predicted_height',
                'method'
            ).latest('date')
            if measurement_system == 'SI':
                predicted_height = predicted_height.cm
            elif measurement_system == 'Imp':
                predicted_height = predicted_height.inch
        except PredictedHeight.DoesNotExist:
            try:
                # If not DNA test, latest KHR result
                predicted_height, prediction_method = obj.predictedheight_set.filter(
                    method='khr'
                ).values_list(
                    'predicted_height',
                    'method'
                ).latest('date')
                if measurement_system == 'SI':
                    predicted_height = predicted_height.cm
                elif measurement_system == 'Imp':
                    predicted_height = predicted_height.inch
            except PredictedHeight.DoesNotExist:
                # Return nada if not even KHR result
                predicted_height = None
                prediction_method = None

        try:
            # Latest BioAge is always the best
            bio_age = obj.bioage_set.values_list('bio_age', flat=True).latest('created')
        except BioAge.DoesNotExist:
            bio_age = None

        return {
            'player_id': obj.id,
            'player_name': obj.first_name + ' ' + obj.last_name,
            'lab_key': obj.lab_key,
            'gender': obj.gender,
            'birthday': obj.birthday,
            'current_height': current_height,
            'predicted_height': predicted_height,
            'prediction_method': prediction_method,
            'height_unit': height_unit,
            'height_date': height_date,
            'current_weight': current_weight,
            'weight_unit': weight_unit,
            'bio_age': bio_age,
            'real_age': current_age
        }
