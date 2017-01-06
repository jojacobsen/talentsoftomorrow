from django.conf.urls import url

from . import views


app_name = 'graphs'
urlpatterns = [
    url(r'^height-estimation/$', views.HeightEstimationGraphView.as_view(), name='height-estimation-graph'),
    url(r'^performance/(?P<pk>[0-9]+)/history/$', views.PerformanceHistoricGraphView.as_view(),
        name='performance-history-graph'),
    url(r'^bio-age-performance/(?P<pk>[0-9]+)/latest/$', views.PerformanceBioAgeGraphView.as_view(),
        name='bio-age-performances-graph'),
    url(r'^performance/(?P<pk>[0-9]+)/latest/$', views.PerformanceGraphView.as_view(),
        name='performances-graph'),
]
