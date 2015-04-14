from django.template import Library

from Search.lib import pricelib
from Search.models import SearchItemVoter

register = Library()


@register.filter(name='get_buying_price')
def get_buying_price(search_item):
    price = pricelib.Price(search_item, SearchItemVoter)

    return price.get_price_for_date(search_item.owner_updated_at)


@register.filter(name='get_price_difference')
def get_price_difference(search_item):
    price = pricelib.Price(search_item, SearchItemVoter)

    current_price = price.get_current_price()
    buying_price = search_item.price_at_owner_change

    return current_price - buying_price


@register.assignment_tag(takes_context=True)
def price_difference(context, search_item):
    return get_price_difference(search_item)