from django.template import Library

from GoogleSocialSearch.lib.integer import num_encode

register = Library()


@register.filter(name='num_encode')
def num_encode(number):
    return num_encode(number)