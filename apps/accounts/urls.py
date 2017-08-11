from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from . import views


app_name = 'accounts'
urlpatterns = [
    url(r'^token-auth/$', obtain_jwt_token),
    url(r'^token-refresh/$', refresh_jwt_token),
    url(r'^player/list/$', views.PlayerListView.as_view(), name='players-list'),
    url(r'^player/create/$', views.PlayerCreateView.as_view(), name='players-create'),
    url(r'^player/invite/(?P<pk>[0-9]+)/$', views.PlayerInviteView.as_view(), name='player-invite'),
    url(r'^player/(?P<pk>[0-9]+)/$', views.PlayerView.as_view(), name='player'),
    url(r'^coach/list/$', views.CoachListView.as_view(), name='coaches-list'),
    url(r'^user/$', views.UserDetailView.as_view(), name='user-detail'),
    url(r'^team/create/$', views.TeamCreateView.as_view(), name='team-create'),
    url(r'^team/list/$', views.TeamListView.as_view(), name='team-list'),
    url(r'^team/(?P<pk>[0-9]+)/$', views.TeamView.as_view(), name='team'),
    url(r'^state/$', views.AccountState.as_view(), name='account-state'),
]
