from django.db import models
from django_measurement.models import MeasurementField
from measurement.measures import Weight, Distance
from accounts.models import Player
from django.contrib.postgres.fields import JSONField


class Height(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()
    height = MeasurementField(measurement=Distance, unit_choices=[("cm", "cm")])

    def __str__(self):
        return self.player.user.username


class Weight(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()
    weight = MeasurementField(measurement=Weight, unit_choices=[("kg", "kg")])

    def __str__(self):
        return self.player.user.username


class PredictedHeight(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()
    height = MeasurementField(measurement=Distance, unit_choices=[("cm", "cm")])
    METHOD_CHOICES = (
        ('dna', 'DNA Test'),  # DNA Test has always priority
        ('khr', 'Khamis Roche'),
    )
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)

    def __str__(self):
        return self.player.user.username


class ParentsHeight(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    fathers_height = MeasurementField(measurement=Distance, unit_choices=[("cm", "cm")])
    mothers_height = MeasurementField(measurement=Distance, unit_choices=[("cm", "cm")])

    def __str__(self):
        return self.player.user.username


class BioAge(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    predicted_height = models.ForeignKey(PredictedHeight, on_delete=models.CASCADE)
    current_height = models.ForeignKey(Height, on_delete=models.CASCADE)
    bio_age = models.DecimalField(max_digits=20, decimal_places=10)
    slope_to_bio_age = JSONField(default=list())
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.player.user.username





