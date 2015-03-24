from django.template import Library

from Jooglin.lib import integer

register = Library()


@register.filter(name='num_encode')
def num_encode(number):
    return integer.num_encode(number)


@register.filter(name='num_decode')
def num_decode(string):
    return integer.num_decode(string)