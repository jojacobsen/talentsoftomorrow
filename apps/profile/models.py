from django.db import models
from accounts.models import Player
from django.contrib.postgres.fields import JSONField



class Profile(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)


class BioAge(models.Model):
    bio_age = models.DecimalField(max_digits=20, decimal_places=10)
    slope_to_bio_age = JSONField(default=list())
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.player.user.username





