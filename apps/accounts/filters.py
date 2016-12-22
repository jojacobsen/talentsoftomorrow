import django_filters
from rest_framework import filters
from .models import Player


class PlayerFilter(filters.FilterSet):
    min_birthday = django_filters.DateFilter(name='birthday', lookup_expr='gte')
    max_birthday = django_filters.DateFilter(name='birthday', lookup_expr='lte')

    class Meta:
        model = Player
        fields = ['min_birthday', 'max_birthday']
