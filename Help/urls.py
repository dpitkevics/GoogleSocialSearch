from django.conf.urls import patterns, url

from Help import views

urlpatterns = patterns('',
                       url(r'^levels/$', views.user_levels, name='user_levels'),
                       )