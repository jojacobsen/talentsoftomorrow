from django.conf.urls import url

from . import views


app_name = 'questionnaire'
urlpatterns = [
    url(r'^$', views.QuestionnaireView.as_view(), name='overview'),
    url(r'^(?P<pk>[0-9]+)/$', views.QuestionnaireFormView.as_view(),
        name='wizard')
]

