import datetime
from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from profile.models import Height, PredictedHeight, BioAge
from performance.models import Benchmark


class PlayerProfileSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        p = dict()
        # Loop trough the club's measurements
        for m in obj.club.measurements.filter():
            # Get the two latest performance results
            t = obj.performance_set.filter(measurement=m).order_by('-date')[:2]
            if t:
                test = t[0]
                try:
                    # Check if performance is benchmarked
                    b = test.benchmark_set.get()
                    benchmark = {
                        'real_age': b.benchmark,
                        'bio_age': b.benchmark_bio
                    }
                except Benchmark.DoesNotExist:
                    benchmark = None

                if len(t) > 1:
                    if m.smaller_is_better:
                        if t[0].value < t[1].value:
                            progress = 'up'
                        elif t[0].value > t[1].value:
                            progress = 'down'
                        else:
                            progress = 'constant'
                    else:
                        if t[0].value > t[1].value:
                            progress = 'up'
                        elif t[0].value < t[1].value:
                            progress = 'down'
                        else:
                            progress = 'constant'
                else:
                    progress = 'constant'

                t = {
                    'value': test.value,
                    'measurement': test.measurement.id,
                    'name': test.measurement.name,
                    'slug': test.measurement.slug_name,
                    'unit': test.measurement.unit.abbreviation,
                    'benchmark': benchmark,
                    'progress': progress
                }

                p.setdefault(test.measurement.category, []).append(t)

        try:
            current_height, height_date = obj.height_set.values_list('height', 'date').latest('date')
            # Uses the date when height was recorded
            current_age = round((height_date - obj.birthday).days / 365.25, 1)
            if obj.club.measurement_system == 'SI':
                current_height = current_height.cm
                height_unit = 'cm'
            elif obj.club.measurement_system == 'Imp':
                current_height = current_height.inch
                height_unit = 'inch'
        except Height.DoesNotExist:
            current_height = None
            current_age = round((datetime.date.today() - obj.birthday).days / 365.25, 1)

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
                predicted_height = None
                prediction_method = None

        try:
            # Latest BioAge is always the best
            bio_age = obj.bioage_set.values_list('bio_age', flat=True).latest('created')
        except BioAge.DoesNotExist:
            bio_age = None

        player = {
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
            'bio_age': bio_age,
            'real_age': current_age
        }
        return {
            'data': p,
            'player': player,
        }
