from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.auth.models import User
from fernet_fields import EncryptedTextField
from django.contrib.postgres.fields import JSONField, ArrayField


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/uuid/<filename>
    u = uuid.uuid4()
    return 'images/profile/' + '/user_{0}/{1}/{2}'.format(instance.user.id, u.hex, filename)


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


class DnaMeasurement(models.Model):
    name = models.CharField(max_length=300)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    slug_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=2000)
    upper_limit = models.DecimalField(max_digits=16, decimal_places=10)
    lower_limit = models.DecimalField(max_digits=16, decimal_places=10)

    def __str__(self):
        return self.name + ' in ' + self.unit.name


class Measurement(models.Model):
    name = models.CharField(max_length=300)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    slug_name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    upper_limit = models.DecimalField(max_digits=16, decimal_places=10)
    lower_limit = models.DecimalField(max_digits=16, decimal_places=10)
    statistic_array = ArrayField(ArrayField(models.FloatField()))
    GROUP_CHOICES = (
        ('test', 'test'),
        ('anthro', 'anthropometric'),
        ('ment', 'mentality'),
        ('skill', 'skill'),
    )
    group = models.CharField(max_length=10, choices=GROUP_CHOICES)
    related_dna_measurement = models.ForeignKey(DnaMeasurement, on_delete=models.CASCADE, blank=True, null=True)
    factor_to_dna_measurement = models.FloatField(default=1, blank=True, null=True)
    # TODO: what if smaller is better?
    # TODO: get_value with limited decimal places

    def __str__(self):
        return self.name + ' in ' + self.unit.name


class Club(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    measurements = models.ManyToManyField(Measurement, blank=True)

    def __str__(self):
        return self.user.username


class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    lab_key = models.CharField(max_length=100, unique=True)
    birthday = models.DateField()
    first_name = EncryptedTextField()
    last_name = EncryptedTextField()
    active = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return self.user.username


class ProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url = models.ImageField(upload_to=user_directory_path)

    def __str__(self):
        return self.user.username


class Performance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=20, decimal_places=10)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    description = models.CharField(max_length=2000, blank=True)

    def __str__(self):
        return self.player.user.username


class PerformanceAnalyse(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    bio_age = models.DecimalField(max_digits=20, decimal_places=10)
    slope_to_bio_age = JSONField(default=list())
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.player.user.username


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


class PerformanceBenchmark(models.Model):
    benchmark = models.DecimalField(max_digits=6, decimal_places=3)  # Benchmark compared to real Age
    benchmark_bio = models.DecimalField(max_digits=6,
                                        decimal_places=3, blank=True, null=True)  # Benchmark compared to Bio Age
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.performance.player.user.username
