from django.conf.urls import url

from . import views


app_name = 'graphs'
urlpatterns = [
    url(r'^height_estimation/$', views.HeightEstimationListView.as_view(), name='height-estimation-list'),
    url(r'^performance_history/(?P<pk>[0-9]+)/$', views.PerformanceHistoricListView.as_view(),
        name='historic-list'),
    url(r'^performance_to_bio_age/(?P<pk>[0-9]+)/$', views.PerformanceToBioAgeListView.as_view(),
        name='performances-to-bio-age-list'),

]
