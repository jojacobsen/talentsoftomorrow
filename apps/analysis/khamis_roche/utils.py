from analysis.calculate import RscriptAnalysis
from analysis.models import KhamisRoche
from profile.models import Height, Weight, ParentsHeight


def create_khamis_roche(sender, instance, created):
    """
    Calculates KHR height and stores/modifies Object.
    :param sender:
    :param instance:
    :param created:
    :return:
    """
    if sender == Height:
        current_height = instance
    else:
        # Get latest height record
        try:
            current_height = instance.player.height_set.filter().latest('date')
        except Height.DoesNotExist:
            return False

    if sender == Weight:
        # Use current instance
        current_weight = instance
    else:
        # Get latest weight record
        try:
            current_weight = instance.player.weight_set.filter().latest('date')
        except Weight.DoesNotExist:
            return False

    if sender == ParentsHeight:
        # Use current instance
        parents_height = instance
    else:
        # Get parents height
        try:
            parents_height = instance.player.parentsheight_set.filter().latest('created')
        except ParentsHeight.DoesNotExist:
            return False

    if not (parents_height == instance or current_height == instance or current_weight == instance):
        # If our relevant data didn't changed or wasn't newly
        # created, why to calculate a new khr?
        return False

    # Median Date between weight and height record
    date = current_height.date + (current_weight.date - current_height.date) / 2

    # Current age based on median Date between weight and height record (rounded to x.5)
    current_age = round(((date - instance.player.birthday).days / 365.25) * 2) / 2

    # Age limit is 8-17.5 years
    if current_age < 8:
        current_age = 8
    elif current_age > 17.5:
        current_age = 17.5

    r = RscriptAnalysis()
    # Get predicted height from R script
    predicted_height, meta = r.get_khamis_roche(current_height.height.cm, current_age, current_weight.weight.kg,
                                                parents_height.fathers_height.cm, parents_height.mothers_height.cm,
                                                instance.player.get_gender_display())
    if not predicted_height:
        # Something went wrong
        return False

    if created:
        # Creates KHR Object
        KhamisRoche.objects.create(player=instance.player, predicted_height=predicted_height,
                                   current_height=current_height, current_weight=current_weight,
                                   parents_height=parents_height, meta=meta, date=date)
        return True
    else:
        # Updates predicted height
        # (Does not use update() method because of signals)
        khr = instance.player.khamisroche_set.filter(
            current_height=current_height,
            current_weight=current_weight,
            parents_height=parents_height
        )[0]
        khr.predicted_height = predicted_height
        khr.meta = meta
        khr.date = date
        khr.save()
        return True
