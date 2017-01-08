from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from django_measurement.models import MeasurementField
from accounts.models import Player
from measurement.measures import Distance


class DnaHeight(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()  # Date in DNA file
    predicted_height = MeasurementField(measurement=Distance, unit_choices=[("cm", "cm")])
    meta = JSONField(default=dict())
    original_filename = models.CharField(max_length=2000)

    def __str__(self):
        return self.player.user.username
