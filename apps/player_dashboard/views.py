from .utils import get_latest_rpe, get_number_of_submissions, get_date_first_submission

from django.core.exceptions import ImproperlyConfigured
from django.views import generic
from django.contrib import messages
import datetime
from django.utils.translation import ugettext as _


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
                group = self.request.user.groups.values_list('name', flat=True)
                if 'Club' in group:
                    messages.add_message(self.request, messages.INFO, _('Please login with your Player Account.'))
                    return ['registration/login.html']
                elif 'Coach' in group:
                    messages.add_message(self.request, messages.INFO, _('Please login with your Player Account.'))
                    return ['registration/login.html']
                elif 'Player' in group:
                    return [self.template_name]
                else:
                    messages.add_message(self.request, messages.INFO, _('Please login with your Player Account.'))
                    return ['registration/login.html']
            else:
                return ['registration/login.html']

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated():
            return {}
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            return {}
        elif 'Coach' in group:
            return {}
        elif 'Player' in group:
            context['menu_item'] = 'index'
            context['latest_rpe'] = get_latest_rpe(self.request.user.player)
            context['count_training_session'] = get_number_of_submissions(self.request.user.player, 'training-session')
            context['count_daily_wellbeing'] = get_number_of_submissions(self.request.user.player, 'daily-wellbeing-u15')
            context['completion_daily_wellbeing'] = int((context['count_daily_wellbeing'] / (
                datetime.date.today() - get_date_first_submission(self.request.user.player, 'daily-wellbeing-u15')
            ).days) * 100)
            return context
        else:
            return {}
