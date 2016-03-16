from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views
from django.views.generic import TemplateView


app_name = 'dashboard'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),
]
