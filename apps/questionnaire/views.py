from django.views import generic
from django.core.exceptions import PermissionDenied

from questionnaire.models import Questionnaire, Submission
from player_dashboard.utils import get_questionnaire_list


class QuestionnaireFormView(generic.DetailView):
    model = Questionnaire
    template_name = 'questionnaire/wizard.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionnaireFormView, self).get_context_data(**kwargs)
        context['link_questionnaire'] = get_questionnaire_list(self.request.user)
        context['menu_item'] = kwargs['object'].slug
        return context


class QuestionnaireView(generic.ListView):
    model = Questionnaire
    template_name = 'questionnaire/overview.html'

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)
        if 'Club' in group:
            return Questionnaire.objects.filter(club=self.request.user.club)
        elif 'Coach' in group:
            return Questionnaire.objects.filter(club=self.request.user.coach.club)
        elif 'Player' in group:
            return Questionnaire.objects.filter(club=self.request.user.player.club)
        else:
            raise PermissionDenied('User has no permission to access user data of player.')

    def get_context_data(self, **kwargs):
        context = super(QuestionnaireView, self).get_context_data(**kwargs)
        context['menu_item'] = 'questionnaire'
        return context


class SubmissionView(generic.ListView):
    model = Submission
    template_name = 'questionnaire/history.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        group = self.request.user.groups.values_list('name', flat=True)
        if 'Player' in group:
            return Submission.objects.filter(player=self.request.user.player, questionnaire__slug=slug)
        else:
            raise PermissionDenied('User has no permission to access user data of player.')

    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        context = super(SubmissionView, self).get_context_data(**kwargs)
        context['questionnaire'] = Questionnaire.objects.get(slug=slug)
        context['menu_item'] = slug + '-history'
        return context
