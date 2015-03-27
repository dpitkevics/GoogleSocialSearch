from django.conf.urls import patterns, url

from User import views

urlpatterns = patterns('',
    url(r'^login$', views.login, name='login'),
    url(r'^get-balance/$', views.get_balance, name='get_balance'),
    url(r'^get-experience/$', views.get_experience, name='get_experience'),
)