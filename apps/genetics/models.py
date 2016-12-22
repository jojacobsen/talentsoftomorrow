from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from accounts.models import Player


class DnaMeasurement(models.Model):
    name = models.CharField(max_length=300)
    slug_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=2000)
    upper_limit = models.DecimalField(max_digits=16, decimal_places=10)
    lower_limit = models.DecimalField(max_digits=16, decimal_places=10)

    def __str__(self):
        return self.name + ' in ' + self.unit.name


class DnaResult(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    dna_measurement = models.ForeignKey(DnaMeasurement, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=20, decimal_places=10)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()
    original_filename = models.CharField(max_length=2000)
    meta = JSONField(default=dict())

    def __str__(self):
        return self.player.user.username
