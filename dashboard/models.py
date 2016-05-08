from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.auth.models import User
from fernet_fields import EncryptedTextField


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


class Measurement(models.Model):
    name = models.CharField(max_length=300)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    slug_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=2000)
    upper_limit = models.DecimalField(max_digits=16, decimal_places=10)
    lower_limit = models.DecimalField(max_digits=16, decimal_places=10)

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
    coaches = models.ManyToManyField(Coach, blank=True)
    birthday = models.DateField(blank=True)
    first_name = EncryptedTextField()
    last_name = EncryptedTextField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return self.user.username


class ProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=user_directory_path)

    def __str__(self):
        return self.user.username


class Performance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=16, decimal_places=10)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    description = models.CharField(max_length=2000, blank=True)

