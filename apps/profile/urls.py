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
    url(r'^sitting-height/create/$', views.SittingHeightCreateView.as_view(),
        name='sitting-height-create'),
    url(r'^height/(?P<pk>[0-9]+)/$', views.HeightView.as_view(),
        name='height'),
    url(r'^weight/(?P<pk>[0-9]+)/$', views.WeightView.as_view(),
        name='weight'),
    url(r'^parents-height/(?P<pk>[0-9]+)/$', views.ParentsHeightView.as_view(),
        name='parents-height'),
    url(r'^sitting-height/(?P<pk>[0-9]+)/$', views.SittingHeightView.as_view(),
        name='sitting-height'),
]
