from rest_framework import serializers
import datetime
from dashboard.models import Performance, Measurement


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance

    def validate(self, data):
        if not (data['measurement'].lower_limit <= data['value'] <= data['measurement'].upper_limit):
            raise serializers.ValidationError('%s is not between %s...%s %s' % (data['value'],
                                                                             data['measurement'].lower_limit,
                                                                             data['measurement'].upper_limit,
                                                                             data['measurement'].unit))
        return data
