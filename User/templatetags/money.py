from django import template

from User.lib import money

register = template.Library()


@register.filter(name='convert_to_money')
def convert_to_money(balance):
    return money.convert_to_money(balance)