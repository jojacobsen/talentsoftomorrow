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
        pk = self.context['view'].kwargs['pk']
        performances = obj.performance_set.filter(measurement__id=pk)
        data = list()
        for p in performances:
            data.append([(p.date - obj.birthday).days / 365.25, p.value])
        data.sort()

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
        pk = self.context['view'].kwargs['pk']
        data = list()
        try:
            value = obj.performance_set.filter(
                measurement__id=pk
            ).values_list(
                'value', flat=True
            ).latest('date')
        except Performance.DoesNotExist:
            value = None
        try:
            # Latest BioAge is always the best
            bio_age = obj.bioage_set.values_list('bio_age', flat=True).latest('created')
        except BioAge.DoesNotExist:
            bio_age = None

        if bio_age and value:
            data.append({
                'x': bio_age,
                'y': value,
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
        pk = self.context['view'].kwargs['pk']
        data = list()
        try:
            value, date = obj.performance_set.filter(
                measurement__id=pk
            ).values_list(
                'value',
                'date'
            ).latest('date')
        except Performance.DoesNotExist:
            value = None
            date = None

        if value and date:
            data.append({
                'x': (date - obj.birthday).days / 365.25,
                'y': value,
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
            current_height, height_date = obj.height_set.values_list('height', 'date').latest('date')
            # Uses the date when height was recorded
            current_age = (height_date - obj.birthday).days / 365.25
        except Height.DoesNotExist:
            return {}

        try:
            # DNA result always highest prio
            predicted_height, prediction_method = obj.predictedheight_set.filter(
                method='dna'
            ).values_list(
                'predicted_height',
                'method'
            ).latest('date')
        except PredictedHeight.DoesNotExist:
            try:
                # If not DNA test, latest KHR result
                predicted_height, prediction_method = obj.predictedheight_set.filter(
                    method='khr'
                ).values_list(
                    'predicted_height',
                    'method'
                ).latest('date')
            except PredictedHeight.DoesNotExist:
                # Return nada if not even KHR result
                return {}

        measurement_system = obj.club.measurement_system
        if measurement_system == 'SI':
            predicted_height = predicted_height.cm
            current_height = current_height.cm
            height_unit = 'cm'
        elif measurement_system == 'Imp':
            predicted_height = predicted_height.inch
            current_height = current_height.inch
            height_unit = 'inch'

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
