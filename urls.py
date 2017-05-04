from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('player_dashboard.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^dna/', include('genetics.urls')),
    url(r'^feed/', include('feed.urls')),
    url(r'^graphs/', include('graphs.urls')),
    url(r'^performance/', include('performance.urls')),
    url(r'^profile/', include('profile.urls')),
    url(r'^questionnaire/', include('questionnaire.urls')),
    url(r'^password/', include('password_reset.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^docs/', include('rest_framework_docs.urls')),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^rosetta/', include('rosetta.urls')),
    ]
