from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^dna/', include('genetics.urls')),
    url(r'^graphs/', include('graphs.urls')),
    url(r'^performance/', include('performance.urls')),
    url(r'^profile/', include('profile.urls')),
    url(r'^docs/', include('rest_framework_docs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
