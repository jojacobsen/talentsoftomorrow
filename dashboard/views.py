from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'dashboard/index.html'

