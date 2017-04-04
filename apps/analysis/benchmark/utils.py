from analysis.calculate import RscriptAnalysis
from performance.models import Performance, Measurement, Benchmark
from profile.models import BioAge
import datetime

def create_benchmark(sender, instance, created):
    """
    Create Benchmark for performance
    :param sender:
    :param instance:
    :param created:
    :return:
    """
    if sender == Performance:
        performance = instance
    else:
        # only Performance updates currently supported
        return False

    try:
        # Get newest BioAge (but should be same date or in a time range of 183 days as performance date)
        bio_age = instance.player.bioage_set.filter(
            current_height__date__lte=(performance.date + datetime.timedelta(days=183))
        ).latest('created')
        bio_age_date = bio_age.current_height.date
    except BioAge.DoesNotExist:
        bio_age = None

    if not bio_age:
        try:
            # Get newest BioAge (but should be same date or older than performance date)
            bio_age = instance.player.bioage_set.filter(method='phv', phv__date__lte=performance.date).latest('created')
            bio_age_date = bio_age.phv.date
        except BioAge.DoesNotExist:
            bio_age = None

    # Uses the date when the measurement was taken
    current_age = (performance.date - instance.player.birthday).days / 365.25

    r = RscriptAnalysis()
    benchmark = r.get_benchmark(performance.value,
                                current_age,
                                performance.measurement.statistic_array,
                                performance.measurement.smaller_is_better)
    if not benchmark:
        # Something went wrong
        return False

    if bio_age:
        # Height measurement can't be older than half a year
        if abs((performance.date - bio_age_date).days) < 183:
            benchmark_bio = r.get_benchmark(instance.value,
                                            float(bio_age.bio_age),
                                            instance.measurement.statistic_array,
                                            instance.measurement.smaller_is_better)
        else:
            benchmark_bio = None
    else:
        benchmark_bio = None

    if created:
        # Creates Benchmark Object
        Benchmark.objects.create(performance=instance,
                                 benchmark=benchmark,
                                 benchmark_bio=benchmark_bio,
                                 bio_age=bio_age)
        return True
    else:
        # Updates the currently used benchmark (.update does not trigger signals!)
        instance.benchmark_set.update(
            benchmark=benchmark,
            benchmark_bio=benchmark_bio
        )
        return True
