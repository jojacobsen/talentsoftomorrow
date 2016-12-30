from rest_framework import serializers, exceptions
from .models import Performance, Measurement, Unit, Benchmark


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance

    def validate(self, data):
        group = self.context['request'].user.groups.values_list('name', flat=True)

        if 'Club' in group:
            if data['player'].club != self.context['request'].user.club:
                raise exceptions.PermissionDenied('Club has no permission to access performance data of player.')
        elif 'Coach' in group:
            if data['player'].club != self.context['request'].user.coach.club:
                raise exceptions.PermissionDenied('Coach has no permission to access performance data of player.')
        elif 'Player' in group:
            raise exceptions.PermissionDenied('Players can not post performance data.')
        else:
            raise exceptions.PermissionDenied('User group not selected.')

        if not (data['measurement'].lower_limit <= data['value'] <= data['measurement'].upper_limit):
            raise serializers.ValidationError('%s is not between %s...%s %s' % (data['value'],
                                                                                data['measurement'].lower_limit,
                                                                                data['measurement'].upper_limit,
                                                                                data['measurement'].unit))
        return data

    def create(self, validated_data):
        performance = Performance.objects.create(**validated_data)
        return performance


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit


class MeasurementSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = Measurement


class PerformancePlayerSerializer(serializers.BaseSerializer):
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
        return p
