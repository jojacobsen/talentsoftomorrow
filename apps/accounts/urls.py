from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from . import views


app_name = 'accounts'
urlpatterns = [
    url(r'^token-auth/$', obtain_jwt_token),
    url(r'^token-refresh/$', refresh_jwt_token),
    url(r'^player/list/$', views.PlayerListView.as_view(), name='players-list'),
    url(r'^player/create/$', views.PlayerCreateView.as_view(), name='players-create'),
    url(r'^player/(?P<pk>[0-9]+)/$', views.PlayerDetailView.as_view(), name='player-detail'),
    url(r'^player/(?P<pk>[0-9]+)/update/$', views.PlayerUpdateView.as_view(), name='player-update'),
    url(r'^coach/list/$', views.CoachListView.as_view(), name='coaches-list'),
    url(r'^user/$', views.UserDetailView.as_view(), name='user-detail'),
    url(r'^team/create/$', views.TeamCreateView.as_view(), name='team-create'),
    url(r'^team/list/$', views.TeamListView.as_view(), name='team-list'),
    url(r'^team/(?P<pk>[0-9]+)/$', views.TeamView.as_view(), name='team'),
]
