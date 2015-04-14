from django.template import Library

from Search.lib import itemlib

register = Library()


@register.filter(name='view_count')
def get_view_count(search_item):
    item_helper = itemlib.ItemHelper(search_item)

    return item_helper.get_view_count()


@register.filter(name='click_count')
def get_click_count(search_item):
    item_helper = itemlib.ItemHelper(search_item)

    return item_helper.get_click_count()


@register.filter(name='upvote_count')
def get_upvote_count(search_item):
    item_helper = itemlib.ItemHelper(search_item)

    return item_helper.get_upvote_count()


@register.filter(name='downvote_count')
def get_downvote_count(search_item):
    item_helper = itemlib.ItemHelper(search_item)

    return item_helper.get_downvote_count()