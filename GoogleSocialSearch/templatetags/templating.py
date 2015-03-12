from django import template

from GoogleSocialSearch.settings import SITE_NAME

register = template.Library()


@register.simple_tag
def title(title_text):
    return "%s - %s" % (title_text, SITE_NAME)