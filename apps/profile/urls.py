from django.conf.urls import url

from . import views


app_name = 'performance'
urlpatterns = [
    url(r'^player/(?P<pk>[0-9]+)/$', views.PlayerProfileView.as_view(),
        name='player-profile'),
    url(r'^height/create/$', views.HeightCreateView.as_view(),
        name='height-create'),
    url(r'^weight/create/$', views.WeightCreateView.as_view(),
        name='weight-create'),
    url(r'^parents-height/create/$', views.ParentsHeightCreateView.as_view(),
        name='parents-height-create'),
]
