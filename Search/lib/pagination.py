import math
from collections import OrderedDict
from urllib.parse import urlencode


class Pagination(object):
    def __init__(self, request, items_count, current_page, items_per_page=10, get_page_variable='p'):
        self.request = request
        self.get = request.GET.copy()

        self.items_count = int(items_count)
        self.current_page = int(current_page)
        self.items_per_page = int(items_per_page)
        self.get_page_variable = get_page_variable

        self.page_count = 0
        self.pages_visible = 5

        self.calculate_page_count()
        self.process_get_variable()

    def calculate_page_count(self):
        self.page_count = math.ceil(self.items_count / self.items_per_page)

    def process_get_variable(self):
        if self.get_page_variable in self.get:
            del self.get[self.get_page_variable]

    def build_uri(self, page_number):
        if page_number == 'first':
            return self.build_http_query(1)

        if page_number == 'current':
            return '#'

        if page_number == 'last':
            return self.build_http_query(self.page_count)

        if page_number == 'previous':
            return self.build_http_query(self.current_page - 1)

        if page_number == 'next':
            return self.build_http_query(self.current_page + 1)

        return self.build_http_query(page_number)

    def build_http_query(self, page_number):
        self.get[self.get_page_variable] = page_number

        return "?%s" % urlencode(OrderedDict(self.get))

    def retrieve_page_array(self):
        page_array = OrderedDict()

        if self.current_page > 1:
            page_array['first'] = 'First'
            page_array['previous'] = 'Previous'

        for i in range((self.current_page - self.pages_visible), self.current_page):
            if i < 1:
                continue
            page_array[i] = i

        page_array['current'] = self.current_page

        for i in range((self.current_page + 1), (self.current_page + 1 + self.pages_visible)):
            if i > self.page_count:
                break

            page_array[i] = i

        if self.current_page < self.page_count:
            page_array['next'] = 'Next'
            page_array['last'] = 'Last'

        return page_array