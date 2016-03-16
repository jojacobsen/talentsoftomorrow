from django.conf.urls import url

from . import views
from django.views.generic import TemplateView


app_name = 'dashboard'
urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
]
