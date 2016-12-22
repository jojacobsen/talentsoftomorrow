from django.conf.urls import url

from . import views


app_name = 'genetics'
urlpatterns = [
    url(r'^result/create/', views.DnaResultCreateView.as_view(), name='dna-result-create'),
    url(r'^result/list/', views.DnaResultListView.as_view(), name='dna-results-list'),
    url(r'^measurement/list/', views.DnaMeasurementListView.as_view(), name='measurements-list'),
]
