from django.views import generic
from django.core.exceptions import PermissionDenied

from questionnaire.models import Questionnaire


class QuestionnaireFormView(generic.DetailView):
    model = Questionnaire
    template_name = 'questionnaire/questionnaire.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionnaireFormView, self).get_context_data(**kwargs)
        context['menu_item'] = 'questionnaire'
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
