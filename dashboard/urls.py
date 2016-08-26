from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'dashboard'
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='dashboard/index.html'), name='index'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^performances/create/', views.PerformancesCreateView.as_view(), name='performances-create'),
    url(r'^performances/list/', views.PerformancesListView.as_view(), name='performances-list'),
    url(r'^performance/(?P<pk>[0-9]+)/$', views.PerformanceDetailView.as_view(), name='performance_detail'),
    url(r'^performance/(?P<pk>[0-9]+)/update/$', views.PerformanceUpdateView.as_view(), name='performance-update'),
    url(r'^performance/(?P<pk>[0-9]+)/delete/$', views.PerformanceDeleteView.as_view(), name='performance-delete'),
    url(r'^measurements/list/', views.MeasurementsListView.as_view(), name='measurements-list'),
    url(r'^players/list/', views.PlayersListView.as_view(), name='players-list'),
    url(r'^players/create/', views.PlayersCreateView.as_view(), name='players-create'),
    url(r'^player/(?P<pk>[0-9]+)/$', views.PlayerDetailView.as_view(), name='player-detail'),
    url(r'^player/(?P<pk>[0-9]+)/update/', views.PlayerUpdateView.as_view(), name='player-update'),
    url(r'^coaches/list/', views.CoachListView.as_view(), name='coaches-list'),
    url(r'^dna-result/create/', views.DnaResultCreateView.as_view(), name='dna-result-create'),
    url(r'^dna-results/list/', views.DnaResultsListView.as_view(), name='dna-results-list'),
    url(r'^dna-measurements/list/', views.DnaMeasurementsListView.as_view(), name='measurements-list'),
    url(r'^graphs/genetic_estimation/', views.PerformanceAnaylseListView.as_view(), name='analyse-list'),
    url(r'^graphs/height_estimation/', views.HeightEstimationListView.as_view(), name='height-estimation-list'),
    url(r'^graphs/performance_history/(?P<pk>[0-9]+)/$', views.PerformancesHistoricListView.as_view(),
        name='historic-list'),
    url(r'^graphs/performance_to_bio_age/(?P<pk>[0-9]+)/$', views.PerformancesToBioAgeListView.as_view(),
        name='performances-to-bio-age-list'),
    url(r'^player/profile/(?P<pk>[0-9]+)/$', views.PlayerProfileView.as_view(),
        name='player-performance-list'),
    url(r'^user/', views.UserDetailView.as_view(), name='user-detail'),
    url(r'^docs/', include('rest_framework_docs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
