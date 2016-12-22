import django_filters
from rest_framework import filters
from .models import Performance


class PerformanceFilter(filters.FilterSet):
    min_birthday = django_filters.DateFilter(name='player__birthday', lookup_expr='gte')
    max_birthday = django_filters.DateFilter(name='player__birthday', lookup_expr='lte')

    class Meta:
        model = Performance
        fields = ['player', 'measurement', 'min_birthday', 'max_birthday']
