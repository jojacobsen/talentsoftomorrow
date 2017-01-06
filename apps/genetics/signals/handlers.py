from django.db.models.signals import post_save
from django.dispatch import receiver
from genetics.models import DnaHeight
from profile.models import PredictedHeight


@receiver(post_save, sender=DnaHeight)
def post_dna_height_handler(sender, instance=None, created=False, **kwargs):
    if created:
        # Creates Height Prediction in Profile App
        PredictedHeight.objects.create(player=instance.player,
                                       date=instance.date,
                                       predicted_height=instance.predicted_height,
                                       method='dna',
                                       khamis_roche=None,
                                       dna_height=instance)
    else:
        # Updates Height Prediction in Profile App
        # (Does not use update() method because of signals)
        prediction = instance.player.predictedheight_set.filter(
            dna_height=instance
        )[0]
        prediction.date = instance.date
        prediction.predicted_height = instance.predicted_height
        prediction.save()
