from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")


@register.assignment_tag(takes_context=True)
def settings_context(context, name):
    return settings_value(name)
