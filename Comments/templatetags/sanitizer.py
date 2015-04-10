from django.template import Library

import bleach

register = Library()


@register.filter(name='sanitize')
def sanitize(text, tags=bleach.ALLOWED_TAGS, attrs=bleach.ALLOWED_ATTRIBUTES, styles=bleach.ALLOWED_STYLES):
    cleaned_text = bleach.clean(text, tags, attrs, styles)

    return cleaned_text