from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from Jooglin import settings

from Search.admin import user_admin_site

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('Search.urls', namespace='Search')),
    url(r'^user/', include('User.urls', namespace='User')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user-admin/', include(user_admin_site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_URL)