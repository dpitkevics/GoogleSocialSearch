from django import template
from django.core.exceptions import ObjectDoesNotExist

from Search.models import SearchItemVoter

register = template.Library()

@register.filter(name='can_vote')
def can_vote(search_item, user):
    try:
        SearchItemVoter.objects.get(search_item=search_item, user=user)

        return False
    except ObjectDoesNotExist:
        return True