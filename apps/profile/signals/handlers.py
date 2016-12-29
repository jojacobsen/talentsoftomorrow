from django.db.models.signals import post_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta
import decimal
from analysis.khamis_roche.utils import create_khamis_roche
from profile.models import Height, Weight, ParentsHeight


@receiver(post_save, sender=Height)
def post_current_height_handler(sender, instance=None, created=False, **kwargs):
    create_khamis_roche(sender, instance, created)


@receiver(post_save, sender=Weight)
def post_current_weight_handler(sender, instance=None, created=False, **kwargs):
    create_khamis_roche(sender, instance, created)


@receiver(post_save, sender=ParentsHeight)
def post_parents_height_handler(sender, instance=None, created=False, **kwargs):
    create_khamis_roche(sender, instance, created)
