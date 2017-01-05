import datetime
from analysis.calculate import RscriptAnalysis
from profile.models import PHV, SittingHeight, Height, Weight


def create_phv(sender, instance, created):
    """
    Calculates PHV date and stores/modifies Object.
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

    if sender == SittingHeight:
        # Use current instance
        sitting_height = instance
    else:
        # Get parents height
        try:
            sitting_height = instance.player.sittingheight_set.filter().latest('date')
        except SittingHeight.DoesNotExist:
            return False

    # Median Date between weight and height record
    date = sitting_height.date + ((current_height.date + (current_weight.date - current_height.date) / 2)
                                  - sitting_height.date) / 1.5

    # Current age based on median Date between weight and height record
    current_age = (date - instance.player.birthday).days / 365.25

    r = RscriptAnalysis()
    # Get distance to PHV in years
    phv_delta = r.get_phv(current_height.height.cm, current_age, current_weight.weight.kg,
                          sitting_height.sitting_height.cm)

    phv_date = date - datetime.timedelta(days=(phv_delta * 365.25))
    if created:
        # Creates a new phv object
        PHV.objects.create(player=instance.player,
                           phv_date=phv_date,
                           current_height=current_height,
                           current_weight=current_weight,
                           sitting_height=sitting_height,
                           date=date)
        return True
    else:
        # Updates the currently used PHV object (.update does not trigger signals!)
        instance.player.phv_set.filter(
            current_height=current_height,
            current_weight=current_weight,
            sitting_height=sitting_height
        ).update(
            phv_date=phv_date,
            date=date
        )
        return True
