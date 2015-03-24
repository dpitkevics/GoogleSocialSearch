from django.core.exceptions import ObjectDoesNotExist

from Search.models import SearchPlugin
from Jooglin.lib.classes import str_to_class


class AbstractPlugin(object):
    def __init__(self, request):
        self.request = request

    @staticmethod
    def load_plugin(request):
        query = request.GET['query']
        if 'site' in query:
            query_parts = query.split(' ')
            site_link = query_parts[-1]
            query = 'site :link:'
            try:
                search_plugin = SearchPlugin.objects.get(query=query)
                search_plugin_instance = str_to_class(search_plugin.package, search_plugin.class_name)(request, site_link)
            except ObjectDoesNotExist:
                search_plugin_instance = None

            return search_plugin_instance

        try:
            search_plugin = SearchPlugin.objects.get(query=query)
            search_plugin_instance = str_to_class(search_plugin.package, search_plugin.class_name)(request)
        except ObjectDoesNotExist:
            search_plugin_instance = None

        return search_plugin_instance

    def render(self):
        raise NotImplementedError("Render method should be implemented")