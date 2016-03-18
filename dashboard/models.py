from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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
    coach = models.ManyToManyField(Coach, blank=True)
    date_of_birth = models.DateField(blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return self.user.username


class Measurement(models.Model):
    name = models.CharField(max_length=300)
    unit = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    upper_limit = models.DecimalField(max_digits=16, decimal_places=10)
    lower_limit = models.DecimalField(max_digits=16, decimal_places=10)

    def __str__(self):
        return self.name


class Performance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=16, decimal_places=10)
    date = models.DateField(auto_now_add=True)
