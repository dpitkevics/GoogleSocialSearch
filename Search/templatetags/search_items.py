from django.template import Library

from urllib.parse import urlparse, parse_qs

register = Library()


@register.filter(name='is_user_favourite')
def is_user_favourite(item, user):
    return item.is_user_favourite(user)


@register.filter(name='get_youtube_url')
def get_youtube_url(item):
    parsed_link = urlparse(item.link)
    try:
        query_v = parse_qs(parsed_link.query)['v'][0]
    except IndexError:
        return None

    youtube_url = "http://www.youtube.com/embed/%s" % query_v
    return youtube_url