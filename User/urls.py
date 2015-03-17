from django.conf.urls import patterns, url

from User import views

urlpatterns = patterns('',
    url(r'^login$', views.login, name='login'),
)