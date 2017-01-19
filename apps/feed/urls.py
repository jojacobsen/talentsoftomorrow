from django.conf.urls import url

from . import views


app_name = 'feed'
urlpatterns = [
    url(r'^dashboard/$', views.FeedDashboardView.as_view(), name='feed-dashboard'),
    url(r'^player/(?P<pk>[0-9]+)/$', views.FeedPlayerView.as_view(),
        name='feed-player'),
]
