from rest_framework import serializers, exceptions
from performance.models import Performance, Measurement, Unit, Benchmark


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'

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
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = Measurement
        fields = '__all__'


class PerformancePlayerSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        p = dict()
        benchmark_bio = list()
        benchmark_chrono = list()
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
                    benchmark_chrono.append(float(b.benchmark))
                    if b.benchmark_bio:
                        benchmark_bio.append(float(b.benchmark_bio))
                    else:
                        benchmark_bio.append(50.0)
                except Benchmark.DoesNotExist:
                    benchmark = None
                    # Fallback benchmark is 50%
                    benchmark_bio.append(50.0)
                    benchmark_chrono.append(50.0)

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
            else:
                # Fallback benchmark is 50%
                benchmark_bio.append(50.0)
                benchmark_chrono.append(50.0)

        # Calculate averages
        p['benchmark_chrono_ave'] = sum(benchmark_chrono) / float(len(benchmark_chrono))
        p['benchmark_bio_ave'] = sum(benchmark_bio) / float(len(benchmark_bio))
        return p


class BenchmarkSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        benchmark_bio = list()
        benchmark_chrono = list()
        # Loop trough the club's measurements
        for m in obj.club.measurements.filter():
            # Get the two latest performance results
            try:
                t = obj.performance_set.filter(measurement=m).latest('date')
            except Performance.DoesNotExist:
                # Fallback benchmark is 50%
                benchmark_bio.append(50.0)
                benchmark_chrono.append(50.0)
                continue
            try:
                # Check if performance is benchmarked
                b = t.benchmark_set.get()
                benchmark_chrono.append(float(b.benchmark))
                if b.benchmark_bio:
                    benchmark_bio.append(float(b.benchmark_bio))
                else:
                    benchmark_bio.append(50.0)
            except Benchmark.DoesNotExist:
                # Fallback benchmark is 50%
                benchmark_bio.append(50.0)
                benchmark_chrono.append(50.0)

        # Calculate averages
        benchmark_chrono_ave = sum(benchmark_chrono) / float(len(benchmark_chrono))
        benchmark_bio_ave = sum(benchmark_bio) / float(len(benchmark_bio))
        return {
            'player': obj.id,
            'benchmark_chrono_ave': benchmark_chrono_ave,
            'benchmark_bio_ave': benchmark_bio_ave
        }

