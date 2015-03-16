from django.conf.urls import patterns, url

from Search import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^suggestion/$', views.suggestion, name='suggestion'),
    url(r'^open/(?P<url>\w+)/$', views.suggestions, name='open'),
)