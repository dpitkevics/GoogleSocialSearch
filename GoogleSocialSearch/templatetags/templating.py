from django import template

from GoogleSocialSearch.settings import SITE_NAME

register = template.Library()


@register.simple_tag
def title(title_text):
    if len(title_text) > 0:
        return "%s - %s" % (title_text, SITE_NAME)

    return SITE_NAME