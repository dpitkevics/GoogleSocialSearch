from django.template import Library


register = Library()


@register.filter(name='get_experience')
def get_experience(user):
    return user.profile.get().experience


@register.filter(name='get_experience_from')
def get_experience_from(user):
    return user.profile.get().experience_level.experience_from


@register.filter(name='get_experience_till')
def get_experience_till(user):
    return user.profile.get().experience_level.experience_till


@register.filter(name='get_experience_percentage')
def get_experience_percentage(user):
    return 100 / (get_experience_till(user) - get_experience_from(user)) * (get_experience(user) - get_experience_from(user))