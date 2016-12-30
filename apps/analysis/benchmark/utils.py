from analysis.calculate import RscriptAnalysis
from performance.models import Performance, Measurement, Benchmark
from profile.models import BioAge


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
        # Latest BioAge is always the best
        bio_age = instance.player.bioage_set.filter().latest('created')
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
        if abs((performance.date - bio_age.current_height.date).days) < 183:
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
        # Updates the currently used bio age
        instance.benchmark_set.update(
            benchmark=benchmark,
            benchmark_bio=benchmark_bio
        )
