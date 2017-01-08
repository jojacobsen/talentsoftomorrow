from django.conf.urls import url

from . import views


app_name = 'genetics'
urlpatterns = [
    url(r'^height/create/', views.DnaHeightCreateView.as_view(), name='dna-height-create'),
]
