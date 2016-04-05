from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views


app_name = 'dashboard'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^performances/', views.PerformancesListView.as_view(), name='performances'),
    url(r'^performance/(?P<pk>[0-9]+)/$', views.PerformanceDetailView.as_view(), name='performance'),
    url(r'^measurements/', views.MeasurementsListView.as_view(), name='measurements'),
    url(r'^players/', views.PlayersListView.as_view(), name='playerlist'),
    url(r'^player/(?P<pk>[0-9]+)/$', views.PlayerDetailView.as_view(), name='playerdetail'),
    url(r'^coaches/', views.CoachListView.as_view(), name='coachlist'),
    url(r'^user/', views.UserDetailView.as_view(), name='userdetail'),
]
