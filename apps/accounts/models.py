import uuid
from django.db import models
from django.contrib.auth.models import User
from fernet_fields import EncryptedTextField


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/uuid/<filename>
    u = uuid.uuid4()
    return 'images/profile/' + '/user_{0}/{1}/{2}'.format(instance.user.id, u.hex, filename)


class Club(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    measurements = models.ManyToManyField('performance.Measurement', blank=True)

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
