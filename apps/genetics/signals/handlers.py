from django.db.models.signals import post_save
from django.dispatch import receiver
import decimal
from performance.models import Performance
from .models import DnaResult
from analytics.models import BioAge, Benchmark
from dashboard.utils import RscriptAnalysis


@receiver(post_save, sender=DnaResult)
def post_dna_result_handler(sender, instance=None, created=False, **kwargs):
    if instance.dna_measurement.slug_name == 'gheight_m_estimate':
        if Performance.objects.filter(measurement__related_dna_measurement=instance.dna_measurement,
                                      player=instance.player):
            current_height = Performance.objects.filter(
                measurement__related_dna_measurement=instance.dna_measurement,
                player=instance.player
            ).order_by('-date').first()

            current_height = current_height.value * \
                             decimal.Decimal(current_height.measurement.factor_to_dna_measurement)

            predicted_height = instance.value

            r_scripts = RscriptAnalysis()
            bio_age, slope = r_scripts.get_bio_age(predicted_height, current_height)
            if bio_age and slope:
                BioAge.objects.create(
                    player=instance.player,
                    bio_age=bio_age,
                    slope_to_bio_age=slope
                )
