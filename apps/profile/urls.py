from django.conf.urls import url

from . import views


app_name = 'performance'
urlpatterns = [
    url(r'^player/(?P<pk>[0-9]+)/$', views.PlayerProfileView.as_view(),
        name='player-profile'),
]
