from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.validators import MaxLengthValidator, MinLengthValidator, validate_slug
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
    slug_name = models.CharField(max_length=100, validators=[validate_slug])
    description = models.CharField(max_length=2000)
    category = models.CharField(max_length=100, default='test', validators=[validate_slug])
    precision = models.IntegerField(default=2,
                                    help_text='How many decimals should be shown in Webapp?')
    upper_limit = models.DecimalField(max_digits=16, decimal_places=10, help_text='Highest possible value.')
    lower_limit = models.DecimalField(max_digits=16, decimal_places=10, help_text='Lowest possible value.')
    statistic_array = JSONField(validators=[MinLengthValidator(3), MaxLengthValidator(3)],
                                default=list([[], [], []]),
                                help_text="Use the following format (age, average, SD) "
                                          "with all the same length: "
                                          "[[9,10,11],[3,3.5,4],[2,2,2]].")
    smaller_is_better = models.BooleanField(default=False)
    data = JSONField(default=dict(), help_text="Arbitrary Json Field", blank=True)

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

    def limit_decimals(self):
        return round(self.value, self.measurement.precision)


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

