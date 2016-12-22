from django.db.models.signals import post_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta
import decimal
from performance.models import Performance
from genetics.models import DnaResult
from analytics.models import BioAge, Benchmark
from dashboard.utils import RscriptAnalysis


@receiver(post_save, sender=Performance)
def post_performance_result_handler(sender, instance=None, created=False, **kwargs):
    r_scripts = RscriptAnalysis()

    if instance.measurement.slug_name == 'height':
        if DnaResult.objects.filter(dna_measurement=instance.measurement.related_dna_measurement,
                                    player=instance.player):
            predicted_height = DnaResult.objects.filter(
                dna_measurement=instance.measurement.related_dna_measurement,
                player=instance.player
            ).order_by('-date').first()

            current_height = instance.value * \
                             decimal.Decimal(instance.measurement.factor_to_dna_measurement)

            bio_age, slope = r_scripts.get_bio_age(predicted_height.value, current_height)
            if bio_age and slope:
                BioAge.objects.create(player=instance.player,
                                                  bio_age=bio_age,
                                                  slope_to_bio_age=slope
                                                  )

    rel = relativedelta(instance.date, instance.player.birthday)
    age = rel.years + rel.months / 12 + rel.days / 365.25
    benchmark = r_scripts.get_benchmark(instance.value,
                                        age,
                                        instance.measurement.statistic_array,
                                        instance.measurement.smaller_is_better)

    if instance.player.performanceanalyse_set.filter().order_by('-created')[0]:
        performance_analyse = instance.player.performanceanalyse_set.filter().order_by('-created')[0]
        benchmark_bio = r_scripts.get_benchmark(instance.value,
                                                float(performance_analyse.bio_age),
                                                instance.measurement.statistic_array,
                                                instance.measurement.smaller_is_better)
    else:
        benchmark_bio = None

    Benchmark.objects.create(performance=instance, benchmark=benchmark, benchmark_bio=benchmark_bio)


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
