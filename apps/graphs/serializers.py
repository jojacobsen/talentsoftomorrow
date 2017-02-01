from rest_framework import serializers
from performance.models import Performance
from profile.models import Height, Weight, PredictedHeight, BioAge


class PerformanceHistoricSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        """
        Historic Performance graph.
        :param obj:
        :return:
        """
        pk = self.context['pk']
        performances = obj.performance_set.filter(measurement__id=pk)
        data = list()
        for p in performances:
            data.append([round((p.date - obj.birthday).days / 365.25, 2), round(p.value, 2)])
        data.sort()
        if not data:
            return

        return {
            'data': data,
            'player': obj.id,
            'name': obj.first_name + ' ' + obj.last_name,
            'type': 'spline'
        }


class PerformanceBioAgeSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        """
        Performance to BioAge graph.
        :param obj:
        :return:
        """
        pk = self.context['pk']
        data = list()
        try:
            value = obj.performance_set.filter(
                measurement__id=pk
            ).values_list(
                'value', flat=True
            ).latest('date')
        except Performance.DoesNotExist:
            return
        try:
            # Latest BioAge is always the best
            bio_age = obj.bioage_set.values_list('bio_age', flat=True).latest('created')
        except BioAge.DoesNotExist:
            return

        if bio_age and value:
            data.append({
                'x': round(bio_age, 1),
                'y': round(value, 2),
            }
            )

        return {
            'data': data,
            'player': obj.id,
            'name': obj.first_name + ' ' + obj.last_name,
            'type': 'column'
        }


class PerformanceGraphSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        """
        Latest Performance graph.
        :param obj:
        :return:
        """
        pk = self.context['pk']
        data = list()
        try:
            value, date = obj.performance_set.filter(
                measurement__id=pk
            ).values_list(
                'value',
                'date'
            ).latest('date')
        except Performance.DoesNotExist:
            return

        if value and date:
            data.append({
                'x': round((date - obj.birthday).days / 365.25, 1),
                'y': round(value, 2),
            }
            )

        return {
            'data': data,
            'player': obj.id,
            'name': obj.first_name + ' ' + obj.last_name,
            'type': 'column'
        }


class HeightEstimationSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        """
        Height estimation graph.
        :param obj:
        :return:
        """
        try:
            height = obj.height_set.filter().latest('date')
            height_date = height.date
            # Uses the date when height was recorded
            current_age = round((height_date - obj.birthday).days / 365.25, 1)
            current_height, height_unit = height.value_club_unit()
        except Height.DoesNotExist:
            return

        try:
            # DNA result always highest prio
            prediction = obj.predictedheight_set.filter(
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
                return

        data = list()
        # Add current height
        data.append({
            'x': current_age,
            'y': current_height,
            'predicted_height': False,
        }
        )
        # Add height prediction
        data.append({
            'x': 17.5,
            'y': predicted_height,
            'predicted_height': True,
        }
        )
        return {
            'data': data,
            'player': obj.id,
            'height_unit': height_unit,
            'prediction_method': prediction_method,
            'name': obj.first_name + ' ' + obj.last_name,
            'type': 'line'
        }
