from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from django_measurement.models import MeasurementField
from accounts.models import Player
from measurement.measures import Distance


class KhamisRoche(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    predicted_height = MeasurementField(measurement=Distance, unit_choices=[("cm", "cm")])
    current_height = models.ForeignKey('profile.Height', on_delete=models.CASCADE)
    current_weight = models.ForeignKey('profile.Weight', on_delete=models.CASCADE)
    parents_height = models.ForeignKey('profile.ParentsHeight', on_delete=models.CASCADE)
    meta = JSONField(default=dict())
