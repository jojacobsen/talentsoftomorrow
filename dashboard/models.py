from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User


class Club(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)


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
