from django.db.models.signals import post_save
from django.dispatch import receiver
from analysis.khamis_roche.utils import create_khamis_roche
from analysis.bio_age.utils import create_bio_age
from profile.models import Height, Weight, ParentsHeight, PredictedHeight


@receiver(post_save, sender=Height)
def post_current_height_handler(sender, instance=None, created=False, **kwargs):
    # If success create_khamis_roche triggers
    # 'post_predicted_height_handler' as well
    success = create_khamis_roche(sender, instance, created)
    if not success:
        # When KHR wasn't created but there might already be an DNA test
        create_bio_age(sender, instance, created)


@receiver(post_save, sender=Weight)
def post_current_weight_handler(sender, instance=None, created=False, **kwargs):
    success = create_khamis_roche(sender, instance, created)


@receiver(post_save, sender=ParentsHeight)
def post_parents_height_handler(sender, instance=None, created=False, **kwargs):
    success = create_khamis_roche(sender, instance, created)


@receiver(post_save, sender=PredictedHeight)
def post_predicted_height_handler(sender, instance=None, created=False, **kwargs):
    success = create_bio_age(sender, instance, created)
