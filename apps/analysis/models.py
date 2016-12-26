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
    data = JSONField(default=dict())
