from django.conf.urls import url

from . import views


app_name = 'questionnaire'
urlpatterns = [
    url(r'^$', views.QuestionnaireView.as_view(), name='overview'),
    url(r'^list/$', views.QuestionnaireListView.as_view(),
        name='questionnaire-list'),
    url(r'^(?P<slug>[-\w]+)/$', views.QuestionnaireFormView.as_view(),
        name='wizard'),
    url(r'^history/(?P<slug>[-\w]+)/$', views.SubmissionView.as_view(),
        name='history'),
    url(r'^submit/(?P<slug>[-\w]+)/$', views.SubmissionCreateView.as_view(),
        name='submit'),
    url(r'^submission/list/$', views.SubmissionListView.as_view(),
        name='submission-list')
]
