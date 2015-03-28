from django.template import Library

register = Library()


@register.filter(name='is_user_favourite')
def is_user_favourite(item, user):
    return item.is_user_favourite(user)