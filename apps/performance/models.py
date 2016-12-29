from django.db import models
from django.contrib.postgres.fields import ArrayField
from accounts.models import Player
from profile.models import BioAge


class Unit(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=50)
    SYSTEM_CHOICES = (
        ('SI', 'Metric'),
        ('Imp', 'Imperial'),
        ('-', 'None'),
    )
    system = models.CharField(max_length=10, choices=SYSTEM_CHOICES)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    name = models.CharField(max_length=300)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    slug_name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    upper_limit = models.DecimalField(max_digits=16, decimal_places=10)
    lower_limit = models.DecimalField(max_digits=16, decimal_places=10)
    statistic_array = ArrayField(ArrayField(models.FloatField()))  # TODO: Fix this weird thing (Json field?)
    smaller_is_better = models.BooleanField(default=False)
    # TODO: get_value with limited decimal places

    def __str__(self):
        return self.name + ' in ' + self.unit.name


class Performance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=20, decimal_places=10)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    description = models.CharField(max_length=2000, blank=True)

    def __str__(self):
        return self.player.user.username


class Benchmark(models.Model):
    benchmark = models.DecimalField(max_digits=6, decimal_places=3)  # Benchmark compared to real Age
    benchmark_bio = models.DecimalField(max_digits=6,
                                        decimal_places=3,
                                        blank=True,
                                        null=True)  # Benchmark compared to Bio Age
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    bio_age = models.ForeignKey(BioAge, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.performance.player.user.username

