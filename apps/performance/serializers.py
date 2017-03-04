import datetime
from rest_framework import serializers, exceptions
from performance.models import Performance, Measurement, Unit, Benchmark
from profile.models import Height, BioAge


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
        try:
            height = obj.height_set.filter().latest('date')
            height_date = height.date
            # Uses the date when height was recorded
            current_age = round((height_date - obj.birthday).days / 365.25, 1)
        except Height.DoesNotExist:
            current_age = round((datetime.date.today() - obj.birthday).days / 365.25, 1)

        try:
            # Latest BioAge is always the best
            bio_age, bioage_method = obj.bioage_set.values_list('bio_age', 'method').latest('created')
            bio_age = round(bio_age, 1)
        except BioAge.DoesNotExist:
            bio_age = None

        measurements = list()
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
                chrono_b = float(b.benchmark)
                if b.benchmark_bio:
                    bio_b = float(b.benchmark_bio)
                else:
                    bio_b = 50.0
            except Benchmark.DoesNotExist:
                # Fallback benchmark is 50%
                bio_b = 50.0
                chrono_b = 50.0

            benchmark_bio.append(bio_b)
            benchmark_chrono.append(chrono_b)
            measurements.append({
                'id': t.measurement.id,
                'name': t.measurement.name,
                'slug': t.measurement.slug_name,
                'unit': t.measurement.unit.name,
                'unit_abbreviation': t.measurement.unit.abbreviation,
                'data': t.measurement.data,
                'latest_performance': t.limit_decimals(),
                'bio_benchmark': bio_b,
                'age_benchmark': chrono_b
            })

        # Calculate averages
        benchmark_chrono_ave = sum(benchmark_chrono) / float(len(benchmark_chrono))
        benchmark_bio_ave = sum(benchmark_bio) / float(len(benchmark_bio))
        return {
            'player': obj.id,
            'full_name': ' '.join([obj.first_name, obj.last_name]),
            'initials': obj.first_name[0] + obj.last_name[0],
            'current_age': current_age,
            'current_bio_age': bio_age,
            'measurements': measurements,
            'overall_avg': {
                'benchmark_chrono_ave': benchmark_chrono_ave,
                'benchmark_bio_ave': benchmark_bio_ave
            }
        }

