from rest_framework import filters
from .models import Height, Weight, ParentsHeight, SittingHeight


class HeightFilter(filters.FilterSet):
    class Meta:
        model = Height
        fields = ['player__id', 'player__team__id']


class WeightFilter(filters.FilterSet):
    class Meta:
        model = Weight
        fields = ['player__id', 'player__team__id']


class ParentsHeightFilter(filters.FilterSet):
    class Meta:
        model = ParentsHeight
        fields = ['player__id', 'player__team__id']


class SittingHeightFilter(filters.FilterSet):
    class Meta:
        model = SittingHeight
        fields = ['player__id', 'player__team__id']
