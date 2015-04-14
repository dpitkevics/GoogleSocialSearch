from django.shortcuts import render
from django.db import connection

from Jooglin.lib.database import dictfetchall

from Search.lib.abstract_plugin import AbstractPlugin
from Search.models import SearchItem


class Homepage(AbstractPlugin):
    def __init__(self, request):
        super(Homepage, self).__init__(request)

    def render(self):
        if self.request.user.is_authenticated():
            search_items = SearchItem.objects.filter(owner=self.request.user)

            cursor = connection.cursor()

            sql = "SELECT sisr.* " \
                  "FROM search_requests AS sr " \
                  "JOIN user_search_requests AS usr ON usr.search_request_id = sr.id " \
                  "JOIN search_items_search_request AS sisr ON sr.id = sisr.searchrequest_id " \
                  "WHERE usr.user_id = %s " \
                  "GROUP BY sisr.searchrequest_id " \
                  "ORDER BY usr.search_count DESC " \
                  "LIMIT 10"

            cursor.execute(sql, [self.request.user.pk])

            rows = dictfetchall(cursor)

            search_term_list = []
            for row in rows:
                sql = "SELECT sr.search_terms " \
                      "FROM search_requests AS sr " \
                      "JOIN search_items_search_request AS sisr ON sr.id = sisr.searchrequest_id " \
                      "WHERE sisr.searchitem_id = %s " \
                      "LIMIT 3"

                cursor.execute(sql, [row['searchitem_id']])

                search_term_map = dictfetchall(cursor)

                for search_term in search_term_map:
                    search_term_list.append(search_term['search_terms'])

            context = {
                'search_items': search_items,
                'search_term_list': search_term_list,
            }
        else:
            context = {}
        return render(self.request, 'Search/plugins/homepage.html', context)