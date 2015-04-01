from django.conf.urls import patterns, url

from Search import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^load$', views.load_search, name='load'),
    url(r'^load-item/$', views.load_item, name='load_item'),
    url(r'^suggestion/$', views.suggestion, name='suggestion'),
    url(r'^open/(?P<pk>.+)/$', views.open_link, name='open'),
    url(r'^vote/$', views.vote, name='vote'),
    url(r'^score/$', views.load_scores, name='scores'),
    url(r'^comment/add/$', views.add_comment, name='add_comment'),
    url(r'^purchase/$', views.purchase, name='purchase'),
    url(r'^offer/$', views.offer, name='offer'),
    url(r'^flash-messages/$', views.get_messages, name='get_messages'),
    url(r'^favourite/(?P<srpk>.+)/$', views.favourite, name='favourite'),
    url(r'^my-favourites/$', views.my_favourites, name='my_favourites'),
    url(r'^my-items/$', views.my_items, name='my_items'),
    url(r'^my-offers/$', views.my_offers, name='my_offers'),
    url(r'^offer-action/$', views.offer_action, name='offer_action'),
)