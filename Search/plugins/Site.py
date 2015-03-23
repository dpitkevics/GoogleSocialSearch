from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from Search.lib.abstract_plugin import AbstractPlugin
from Search.models import SearchItem

from Comments.forms import CommentForm


class Site(AbstractPlugin):
    def __init__(self, request, site_link):
        super(Site, self).__init__(request)

        self.site_link = site_link

        try:
            search_item = SearchItem.objects.get(link=self.site_link)
        except ObjectDoesNotExist:
            search_item = None

        self.comment_form = CommentForm()

        self.context = {
            'item': search_item,
            'comment_form': self.comment_form
        }

    def render(self):
        return render(self.request, 'Search/plugins/site.html', self.context)