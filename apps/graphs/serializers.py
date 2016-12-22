
from dateutil.relativedelta import relativedelta
from rest_framework import serializers


class PerformanceAnalyseSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        dna = obj.performanceanalyse_set.filter().order_by('-created')[0]
        dna.slope_to_bio_age.sort()
        return {
            'data': dna.slope_to_bio_age,
            'player': obj.id,
            'name': obj.first_name + ' ' + obj.last_name,
            'type': 'spline'
        }


class PerformanceHistoricSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        pk = self.context['view'].kwargs['pk']
        performances = obj.performance_set.filter(measurement__id=pk)

        data = list()
        for p in performances:
            rel = relativedelta(p.date, obj.birthday)
            data.append([rel.years + rel.months / 12 + rel.days / 365.25, p.value])

        data.sort()

        return {
            'data': data,
            'player': obj.id,
            'name': obj.first_name + ' ' + obj.last_name,
            'type': 'spline'
        }


class PerformanceToBioAgeSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        pk = self.context['view'].kwargs['pk']
        p = obj.performance_set.filter(measurement__id=pk).order_by('-date')[0]
        dna = obj.performanceanalyse_set.filter().order_by('-created')[0]
        rel = relativedelta(p.date, obj.birthday)

        data = list()
        data.append({
            'x': rel.years + rel.months / 12 + rel.days / 365.25,
            'y': p.value,
            'bio_age': False,
        }
        )

        data.append({
            'x': dna.bio_age,
            'y': p.value,
            'bio_age': True,
        }
        )

        return {
            'data': data,
            'player': obj.id,
            'name': obj.first_name + ' ' + obj.last_name,
            'type': 'line'
        }


class HeightEstimationSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        m = obj.club.measurements.filter(slug_name='height')[0]
        p = obj.performance_set.filter(measurement__id=m.pk).order_by('-date')[0]
        dna = obj.dnaresult_set.filter().order_by('-date')[0]
        rel = relativedelta(p.date, obj.birthday)

        data = list()
        data.append({
            'x': rel.years + rel.months / 12 + rel.days / 365.25,
            'y': p.value,
            'predicted_height': False,
        }
        )

        data.append({
            'x': 17.5,
            'y': dna.value,
            'predicted_height': True,
        }
        )

        return {
            'data': data,
            'player': obj.id,
            'name': obj.first_name + ' ' + obj.last_name,
            'type': 'line'
        }
