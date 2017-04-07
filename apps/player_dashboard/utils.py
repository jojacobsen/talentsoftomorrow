from questionnaire.models import Questionnaire, Answer, Submission
from django.core.exceptions import PermissionDenied
import datetime

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


def get_number_of_submissions(player, questionnaire_slug):
    return Submission.objects.filter(player=player,
                                     questionnaire__slug=questionnaire_slug).count()


def get_latest_rpe(player):
    try:
        return Answer.objects.values_list('answer', flat=True).get(submission__player=player,
                                                                   question__slug='rpe').latest('date')
    except Answer.DoesNotExist:
        return None


def get_date_first_submission(player, questionnaire_slug):
    try:
        first_submission = Submission.objects.values_list('date', flat=True).get(
            player=player, questionnaire__slug=questionnaire_slug)
    except Submission.DoesNotExist:
        return datetime.date.today() - datetime.timedelta(days=1)
    if first_submission == datetime.date.today():
        return datetime.date.today() - datetime.timedelta(days=1)
    else:
        return first_submission
