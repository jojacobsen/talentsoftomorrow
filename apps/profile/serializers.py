import datetime
from dateutil.relativedelta import relativedelta
from rest_framework import serializers, exceptions
from performance.models import Benchmark


class PlayerProfileSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        p = dict()
        for m in obj.club.measurements.filter():
            t = obj.performance_set.filter(measurement=m).order_by('-date')
            if t:
                test = t[0]
                try:
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

                p.setdefault(test.measurement.group, []).append(t)

        try:
            m = obj.club.measurements.get(slug_name='height')
        except Measurement.DoesNotExist:
            raise exceptions.NotFound('Club profile is not correctly set up. Add height measurement')

        current_height = obj.performance_set.filter(measurement__id=m.pk).order_by('-date')
        if current_height:
            rel = relativedelta(current_height[0].date, obj.birthday)
            height_unit = current_height[0].measurement.unit.abbreviation
            current_height = current_height[0].value
        else:
            current_height = None
            rel = relativedelta(datetime.date.today(), obj.birthday)
            height_unit = None
        dna_height = obj.dnaresult_set.filter().order_by('-date')
        if dna_height:
            dna_height = dna_height[0].value
        else:
            dna_height = None
        b = obj.performanceanalyse_set.filter().order_by('-created')
        if b:
            if hasattr(b, 'bio_age'):
                bio_age = b.bio_age
            else:
                bio_age = None
        else:
            bio_age = None

        player = {
            'player_id': obj.id,
            'player_name': obj.first_name + ' ' + obj.last_name,
            'lab_key': obj.lab_key,
            'gender': obj.gender,
            'birthday': obj.birthday,
            'current_height': current_height,
            'predicted_height': dna_height,
            'height_unit': height_unit,
            'bio_age': bio_age,
            'real_age': rel.years + rel.months / 12 + rel.days / 365.25
        }
        return {
            'data': p,
            'player': player,
        }
