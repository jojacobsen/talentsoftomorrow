from django.db.models.signals import post_save
from django.dispatch import receiver
from analysis.models import KhamisRoche
from profile.models import PredictedHeight


@receiver(post_save, sender=KhamisRoche)
def post_khamis_roche_handler(sender, instance=None, created=False, **kwargs):
    """
    Listens to Khamis Roche Models and add it
    to Height prediction of player profile
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        # Creates Height Prediction in Profile App
        PredictedHeight.objects.create(player=instance.player,
                                       date=instance.date,
                                       predicted_height=instance.predicted_height,
                                       method='khr',
                                       khamis_roche=instance,
                                       dna_height=None)
    else:
        # Updates Height Prediction in Profile App
        instance.player.predictedheight_set.filter(
            khamis_roche=instance
        )[0].update(
            date=instance.date,
            predicted_height=instance.predicted_height
        )

