from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login

from . import views

app_name = 'player_dashboard'
urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout_then_login, {'login_url': '/'}, name='logout'),
]