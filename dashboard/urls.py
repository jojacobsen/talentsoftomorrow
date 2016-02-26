from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name="password_reset"),
]