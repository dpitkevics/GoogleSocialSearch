from urllib.request import urlopen

from django.core.files.base import ContentFile

from social.backends.google import GoogleOAuth2
from social.backends.facebook import FacebookOAuth2
from social.backends.linkedin import LinkedinOAuth
from social.backends.twitter import TwitterOAuth

from User.models import UserProfile


def update_user_social_data(strategy, *args, **kwargs):
    """Set the name and avatar for a user only if is new.
    """

    print('update_user_social_data :: %s' % strategy)
    if not kwargs['is_new']:
        return
 
    full_name = ''
    backend = kwargs['backend']
 
    user = kwargs['user']

    profile = UserProfile.objects.get_or_create(user=user)[0]
 
    if (
        isinstance(backend, GoogleOAuth2)
        or isinstance(backend, FacebookOAuth2)
    ):
        full_name = kwargs['response'].get('name')
    elif (
        isinstance(backend, LinkedinOAuth)
        or isinstance(backend, TwitterOAuth)
    ):
        if kwargs.get('details'):
            full_name = kwargs['details'].get('fullname')
 
    user.full_name = full_name
 
    if isinstance(backend, GoogleOAuth2):
        if kwargs['response'].get('picture'):
            profile.photo = kwargs['response'].get('picture')
            profile.save()
    elif isinstance(backend, FacebookOAuth2):
        fbuid = kwargs['response']['id']
        image_url = 'http://graph.facebook.com/%s/picture?type=large' % fbuid
        profile.photo = image_url
        profile.save()
    elif isinstance(backend, TwitterOAuth):
        if kwargs['response'].get('profile_image_url'):
            image_url = kwargs['response'].get['profile_image_url']

            profile.photo = image_url
            profile.save()
    elif isinstance(backend, LinkedinOAuth):
        if kwargs['response'].get('pictureUrl'):
            image_url = kwargs['response'].get['pictureUrl']

            profile.photo = image_url
            profile.save()
    user.save()