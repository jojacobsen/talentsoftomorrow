from django.db import models
from django_measurement.models import MeasurementField
from measurement.measures import Weight as WeightMeasurement
from measurement.measures import Distance
from accounts.models import Player
from analysis.models import KhamisRoche
from genetics.models import DnaHeight
from django.contrib.postgres.fields import JSONField


class Height(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    height = MeasurementField(measurement=Distance, unit_choices=[("cm", "cm")])

    def __str__(self):
        return self.player.user.username

    def value_club_unit(self):
        measurement_system = self.player.club.measurement_system
        if measurement_system == 'SI':
            return round(self.height.cm, 1), 'cm'
        elif measurement_system == 'Imp':
            return round(self.height.inch, 1), 'inch'


class Weight(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    weight = MeasurementField(measurement=WeightMeasurement, unit_choices=[("kg", "kg")])

    def __str__(self):
        return self.player.user.username

    def value_club_unit(self):
        measurement_system = self.player.club.measurement_system
        if measurement_system == 'SI':
            return round(self.weight.kg, 1), 'kg'
        elif measurement_system == 'Imp':
            return round(self.weight.lb, 1), 'lb'


class PredictedHeight(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    predicted_height = MeasurementField(measurement=Distance, unit_choices=[("cm", "cm")])
    METHOD_CHOICES = (
        ('dna', 'DNA Test'),  # DNA Test has always priority
        ('khr', 'Khamis Roche'),
    )
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    khamis_roche = models.ForeignKey(KhamisRoche, blank=True, null=True)
    dna_height = models.ForeignKey(DnaHeight, blank=True, null=True)

    def __str__(self):
        return self.player.user.username

    def value_club_unit(self):
        measurement_system = self.player.club.measurement_system
        if measurement_system == 'SI':
            return round(self.predicted_height.cm, 1), 'cm'
        elif measurement_system == 'Imp':
            return round(self.predicted_height.inch, 1), 'inch'


class ParentsHeight(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    fathers_height = MeasurementField(measurement=Distance, unit_choices=[("cm", "cm")])
    mothers_height = MeasurementField(measurement=Distance, unit_choices=[("cm", "cm")])

    def __str__(self):
        return self.player.user.username

    def value_club_unit(self):
        measurement_system = self.player.club.measurement_system
        if measurement_system == 'SI':
            return round(self.fathers_height.cm, 1), round(self.mothers_height.cm, 0), 'cm'
        elif measurement_system == 'Imp':
            return round(self.fathers_height.inch, 1), round(self.mothers_height.inch, 0), 'inch'


class SittingHeight(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    sitting_height = MeasurementField(measurement=Distance, unit_choices=[("cm", "cm")])

    def __str__(self):
        return self.player.user.username

    def value_club_unit(self):
        measurement_system = self.player.club.measurement_system
        if measurement_system == 'SI':
            return round(self.sitting_height.cm, 1), 'cm'
        elif measurement_system == 'Imp':
            return round(self.sitting_height.inch, 1), 'inch'


class PHV(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    current_height = models.ForeignKey(Height, on_delete=models.CASCADE)
    current_weight = models.ForeignKey(Weight, on_delete=models.CASCADE)
    sitting_height = models.ForeignKey(SittingHeight, on_delete=models.CASCADE)
    phv_date = models.DateField()
    date = models.DateField()  # Median date of height & weight measurements


class BioAge(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    predicted_height = models.ForeignKey(PredictedHeight, on_delete=models.CASCADE, blank=True, null=True)
    current_height = models.ForeignKey(Height, on_delete=models.CASCADE, blank=True, null=True)
    phv = models.ForeignKey(PHV, on_delete=models.CASCADE, blank=True, null=True)
    bio_age = models.DecimalField(max_digits=20, decimal_places=10)
    slope_to_bio_age = JSONField(default=list())
    created = models.DateTimeField(auto_now_add=True)
    METHOD_CHOICES = (
        ('pre', 'Height Prediction'),  # Height Prediction has always priority
        ('phv', 'Peak Height Velocity'),
    )
    method = models.CharField(max_length=5, choices=METHOD_CHOICES, default=METHOD_CHOICES[0][0])

    def __str__(self):
        return self.player.user.username
