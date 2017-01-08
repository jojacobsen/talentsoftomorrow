from django.conf.urls import url

from . import views


app_name = 'performance'
urlpatterns = [
    url(r'^create/$', views.PerformanceCreateView.as_view(), name='performance-create'),
    url(r'^list/$', views.PerformanceListView.as_view(), name='performance-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.PerformanceDetailView.as_view(), name='performance_detail'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.PerformanceUpdateView.as_view(), name='performance-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.PerformanceDeleteView.as_view(), name='performance-delete'),
    url(r'^measurement/list/$', views.MeasurementListView.as_view(), name='measurement-list'),
    url(r'^player/(?P<pk>[0-9]+)/latest/$', views.PerformancePlayerView.as_view(), name='performances-latest'),
    url(r'^benchmark/latest/$', views.BenchmarkListView.as_view(), name='benchmark-latest-list'),
]
