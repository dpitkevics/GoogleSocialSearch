from django.shortcuts import render

from Search.lib.abstract_plugin import AbstractPlugin


class Homepage(AbstractPlugin):
    def __init__(self, request):
        super(Homepage, self).__init__(request)

    def render(self):
        return render(self.request, 'Search/plugins/homepage.html', {})