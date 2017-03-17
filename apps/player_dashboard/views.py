from django.core.exceptions import ImproperlyConfigured
from django.views import generic
from .utils import get_questionnaire_list


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
        return context
