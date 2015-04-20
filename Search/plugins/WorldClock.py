from django.utils import timezone
from django.shortcuts import render

from Search.lib.abstract_plugin import AbstractPlugin


class WorldClock(AbstractPlugin):

    def render(self):
        self.add_css('test.css')
        print(timezone.now())

        context = {}

        return render(self.request, 'Search/plugins/world_clock.html', context)