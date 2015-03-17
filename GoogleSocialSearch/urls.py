from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from GoogleSocialSearch import settings

urlpatterns = patterns('',
    url(r'^', include('Search.urls', namespace='Search')),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
