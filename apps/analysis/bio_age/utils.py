from analysis.calculate import RscriptAnalysis
from profile.models import BioAge, PredictedHeight, Height


def create_bio_age(sender, instance, created):
    """
    Calculates bio age with latest available values and stores it.
    :param sender:
    :param instance:
    :param created:
    :return:
    """
    try:
        # DNA result always highest prio
        prediction = instance.player.predictedheight_set.filter(method='dna').latest('date')
    except PredictedHeight.DoesNotExist:
        try:
            # If not DNA test, latest KHR result
            prediction = instance.player.predictedheight_set.filter(method='khr').latest('date')
        except PredictedHeight.DoesNotExist:
            # Return nada if not even KHR result
            return False
    try:
        current_height = instance.player.height_set.filter().latest('date')
    except Height.DoesNotExist:
        # Current height is not available
        return False

    if not (prediction == instance or current_height == instance):
        # If our relevant data (latest prediction or current height) didn't
        # changed or wasn't newly created, why to calculate a new bio age?
        return False

    r = RscriptAnalysis()
    bio_age, slope = r.get_bio_age(prediction.predicted_height.cm, current_height.height.cm)

    if created:
        # Creates a new bio age object
        BioAge.objects.create(player=instance.player,
                              predicted_height=prediction,
                              current_height=current_height,
                              bio_age=bio_age,
                              slope_to_bio_age=slope)
        return True
    else:
        # Updates the currently used bio age (.update does not trigger signals!)
        instance.player.bioage_set.filter(
            predicted_height=prediction,
            current_height=current_height,
        ).update(
            bio_age=bio_age,
            slope_to_bio_age=slope
        )
        return True
