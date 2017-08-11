from django.conf.urls import url

from . import views


app_name = 'performance'
urlpatterns = [
    url(r'^create/$', views.PerformanceCreateView.as_view(), name='performance-create'),
    url(r'^list/$', views.PerformanceListView.as_view(), name='performance-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.PerformanceView.as_view(), name='performance'),
    url(r'^measurement/list/$', views.MeasurementListView.as_view(), name='measurement-list'),
    url(r'^player/(?P<pk>[0-9]+)/latest/$', views.PerformancePlayerView.as_view(), name='performances-latest'),
    url(r'^benchmark/latest/$', views.BenchmarkListView.as_view(), name='benchmark-latest-list'),
    url(r'^import/(?P<filename>\w+|[\w.%+-]+\.[A-Za-z]{2,4})/$', views.PerformanceImportView.as_view(),
        name='performance-import'),
    url(r'^template/download/$', views.TemplateDownloadView.as_view(),
        name='template-download'),
]
