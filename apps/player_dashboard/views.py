from django.core.exceptions import ImproperlyConfigured
from django.views import generic
from .utils import get_questionnaire_list, get_latest_rpe, get_number_of_submissions, get_date_first_submission
import datetime


class DashboardView(generic.TemplateView):
    template_name = 'player_dashboard/index.html'

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'"
            )
        else:
            if self.request.user.is_authenticated():
                return [self.template_name]
            else:
                return ['registration/login.html']

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated():
            return {}
        context['link_questionnaire'] = get_questionnaire_list(self.request.user)
        context['menu_item'] = 'index'
        context['latest_rpe'] = get_latest_rpe(self.request.user.player)
        context['count_training_session'] = get_number_of_submissions(self.request.user.player, 'training-session')
        context['count_daily_wellbeing'] = get_number_of_submissions(self.request.user.player, 'daily-wellbeing-u15')
        context['completion_daily_wellbeing'] = int((context['count_daily_wellbeing'] / (
            datetime.date.today() - get_date_first_submission(self.request.user.player, 'daily-wellbeing-u15')
        ).days) * 100)
        return context
