import datetime
from rest_framework import serializers
from profile.models import Height, Weight, PredictedHeight, BioAge, ParentsHeight


class PlayerProfileSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        try:
            height = obj.height_set.filter().latest('date')
            height_date = height.date
            # Uses the date when height was recorded
            current_age = round((height_date - obj.birthday).days / 365.25, 1)
            current_height, height_unit = height.value_club_unit()
        except Height.DoesNotExist:
            current_height = None
            current_age = round((datetime.date.today() - obj.birthday).days / 365.25, 1)

        # Get latest weight record
        try:
            weight = obj.weight_set.filter().latest('date')
            current_weight, weight_unit = weight.value_club_unit()
        except Weight.DoesNotExist:
            current_weight = None
            weight_unit = None

        try:
            # DNA result always highest prio
            prediction, prediction_method = obj.predictedheight_set.filter(
                method='dna'
            ).latest('date')
            prediction_method = 'dna'
            predicted_height, height_unit = prediction.value_club_unit()
        except PredictedHeight.DoesNotExist:
            try:
                # If not DNA test, latest KHR result
                prediction = obj.predictedheight_set.filter(
                    method='khr'
                ).latest('date')
                prediction_method = 'khr'
                predicted_height, height_unit = prediction.value_club_unit()
            except PredictedHeight.DoesNotExist:
                # Return nada if not even KHR result
                predicted_height = None
                prediction_method = None

        # Get parents height
        try:
            parents_height = obj.parentsheight_set.filter().latest('created')
            fathers_height, mothers_height, height_unit = parents_height.value_club_unit()
        except ParentsHeight.DoesNotExist:
            fathers_height = None
            mothers_height = None

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
            'real_age': current_age,
            'fathers_height': fathers_height,
            'mothers_height': mothers_height
        }
