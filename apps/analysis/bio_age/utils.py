from analysis.calculate import RscriptAnalysis, PythonAnalysis
from profile.models import BioAge, PredictedHeight, Height, PHV


def create_bio_age(sender, instance, created):
    """
    Calculates bio age and stores it.
    :param sender:
    :param instance:
    :param created:
    :return:
    """
    if sender == PredictedHeight:
        prediction = instance
    else:
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

    if sender == Height:
        current_height = instance
    else:
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
                              slope_to_bio_age=slope,
                              method='pre')
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


def create_alternative_bio_age(sender, instance, created):
    if sender == PHV:
        phv = instance
    else:
        return False

    # Bio Age based on prediction is better
    if phv.player.bioage_set.filter(method='pre').values_list('created', flat=True):
        return False

    # Current age based on median Date between weight and height record
    current_age = (phv.date - instance.player.birthday).days / 365.25
    phv_age = (phv.phv_date - instance.player.birthday).days / 365.25

    p = PythonAnalysis()
    bio_age = p.get_alternative_bio_age(current_age, phv_age)

    if created:
        # Creates a new bio age object
        BioAge.objects.create(player=instance.player,
                              bio_age=bio_age,
                              phv=instance,
                              method='phv')
        return True
    else:
        # Updates the currently used bio age (.update does not trigger signals!)
        instance.player.bioage_set.filter(
            phv=instance
        ).update(
            bio_age=bio_age,
        )
        return True
