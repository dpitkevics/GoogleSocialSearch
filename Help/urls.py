from django.conf.urls import patterns, url

from Help import views

urlpatterns = patterns('',
                       url(r'^levels/$', views.user_levels, name='user_levels'),
                       url(r'^homepage/$', views.set_as_homepage, name='set_as_homepage'),
                       url(r'^search-engine/$', views.set_as_default_search_engine, name='set_as_default_search'),
                       )