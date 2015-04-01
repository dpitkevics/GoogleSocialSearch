from django import template

from User.lib import money

from Search.models import SearchItem, SearchItemOffer

register = template.Library()


@register.filter(name='convert_to_money')
def convert_to_money(balance):
    return money.convert_to_money(balance)


@register.filter(name='has_pending_offers')
def has_pending_offers(user):
    search_items = SearchItem.objects.filter(owner=user)
    offers_to_me = SearchItemOffer.objects.filter(search_item__in=search_items, offer_status=SearchItemOffer.OFFER_STATUS_PENDING)

    if len(offers_to_me) > 0:
        return True

    return False