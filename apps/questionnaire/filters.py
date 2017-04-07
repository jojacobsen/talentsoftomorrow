import django_filters
from rest_framework import filters
from .models import Submission


class SubmissionFilter(filters.FilterSet):
    min_birthday = django_filters.DateFilter(name='player__birthday', lookup_expr='gte')
    max_birthday = django_filters.DateFilter(name='player__birthday', lookup_expr='lte')

    class Meta:
        model = Submission
        fields = ['player', 'player__team__id', 'questionnaire', 'min_birthday', 'max_birthday']
