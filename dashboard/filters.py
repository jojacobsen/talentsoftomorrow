import django_filters
from rest_framework import filters
from dashboard.models import PerformanceAnalyse, Performance, Player


class PlayerFilter(filters.FilterSet):
    min_birthday = django_filters.DateFilter(name='birthday', lookup_expr='gte')
    max_birthday = django_filters.DateFilter(name='birthday', lookup_expr='lte')

    class Meta:
        model = Player
        fields = ['min_birthday', 'max_birthday']


class PerformanceFilter(filters.FilterSet):
    min_birthday = django_filters.DateFilter(name='player__birthday', lookup_expr='gte')
    max_birthday = django_filters.DateFilter(name='player__birthday', lookup_expr='lte')

    class Meta:
        model = Performance
        fields = ['player', 'measurement', 'min_birthday', 'max_birthday']


class PerformanceAnalyseFilter(filters.FilterSet):
    min_birthday = django_filters.DateFilter(name='player__birthday', lookup_expr='gte')
    max_birthday = django_filters.DateFilter(name='player__birthday', lookup_expr='lte')

    class Meta:
        model = PerformanceAnalyse
        fields = ['player', 'min_birthday', 'max_birthday']
