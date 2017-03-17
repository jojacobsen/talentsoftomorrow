from questionnaire.models import Questionnaire

from django.core.exceptions import PermissionDenied


def get_questionnaire_list(user):
    group = user.groups.values_list('name', flat=True)
    if 'Club' in group:
        return Questionnaire.objects.filter(club=user.club).values_list('name', 'id', 'slug')
    elif 'Coach' in group:
        return Questionnaire.objects.filter(club=user.coach.club).values_list('name', 'id', 'slug')
    elif 'Player' in group:
        return Questionnaire.objects.filter(club=user.player.club).values_list('name', 'id', 'slug')
    else:
        raise PermissionDenied('User has no permission to access user data of player.')