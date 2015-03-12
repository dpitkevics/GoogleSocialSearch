import requests
import json
from urllib.parse import quote

from GoogleSocialSearch import settings


MAX_LOAD_PER_PAGE = 10
MAX_LOAD_PER_RANGE = 100
MAX_TOTAL_LOAD = 1000

LOAD_RANGE = 100


def do_search(query, start=1):
    """
    Executes search and returns formatted objects

    :param query: string
    :return: SearchResult
    """

    if start > MAX_TOTAL_LOAD:
        start = MAX_TOTAL_LOAD

    low_range = start - (start % LOAD_RANGE)
    high_range = low_range + LOAD_RANGE

    real_start = start - low_range

    request_url = "https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s&start=%d&lowRange=%d&highRange=%d" % (
        settings.API_KEY,
        settings.API_SEARCH_CX,
        quote(query),
        real_start,
        low_range,
        high_range
    )

    data = requests.get(request_url)

    search_results = json.loads(data.text)

    if 'error' in search_results:
        print(search_results)
        return None

    search_information = SearchInformation()

    if 'searchInformation' in search_results:
        search_information.search_time = search_results['searchInformation']['searchTime']
        search_information.formatted_search_time = search_results['searchInformation']['formattedSearchTime']
        search_information.total_results = search_results['searchInformation']['totalResults']
        search_information.formatted_total_results = search_results['searchInformation']['formattedTotalResults']

    request = Request()
    next_page = NextPage()
    if 'queries' in search_results:
        if 'request' in search_results['queries']:
            request.title = search_results['queries']['request'][0]['title']
            request.total_results = search_results['queries']['request'][0]['totalResults']
            request.search_terms = search_results['queries']['request'][0]['searchTerms']
            request.count = search_results['queries']['request'][0]['count']
            request.start_index = search_results['queries']['request'][0]['startIndex']
            request.input_encoding = search_results['queries']['request'][0]['inputEncoding']
            request.output_encoding = search_results['queries']['request'][0]['outputEncoding']
            request.safe = search_results['queries']['request'][0]['safe']
            request.cx = search_results['queries']['request'][0]['cx']

        if 'nextPage' in search_results['queries']:
            next_page.title = search_results['queries']['nextPage'][0]['title']
            next_page.total_results = search_results['queries']['nextPage'][0]['totalResults']
            next_page.search_terms = search_results['queries']['nextPage'][0]['searchTerms']
            next_page.count = search_results['queries']['nextPage'][0]['count']
            next_page.start_index = search_results['queries']['nextPage'][0]['startIndex']
            next_page.input_encoding = search_results['queries']['nextPage'][0]['inputEncoding']
            next_page.output_encoding = search_results['queries']['nextPage'][0]['outputEncoding']
            next_page.safe = search_results['queries']['nextPage'][0]['safe']
            next_page.cx = search_results['queries']['nextPage'][0]['cx']

    search_result = SearchResult(search_information=search_information, request=request, next_page=next_page)
    if 'items' in search_results:
        for item in search_results['items']:
            if 'pagemap' in item:
                if 'cse_image' in item['pagemap']:
                    cse_image = CseImage(src=item['pagemap']['cse_image'][0]['src'])
                else:
                    cse_image = None

                if 'cse_thumbnail' in item['pagemap']:
                    cse_thumbnail = CseThumbnail(width=item['pagemap']['cse_thumbnail'][0]['width'],
                                                 height=item['pagemap']['cse_thumbnail'][0]['height'],
                                                 src=item['pagemap']['cse_thumbnail'][0]['src'])
                else:
                    cse_thumbnail = None

                if 'metatags' in item['pagemap']:
                    metatags = Metatags()

                    if 'referrer' in item['pagemap']['metatags'][0]:
                        metatags.referrer = item['pagemap']['metatags'][0]['referrer']

                    if 'og:site_name' in item['pagemap']['metatags'][0]:
                        metatags.site_name = item['pagemap']['metatags'][0]['og:site_name']

                    if 'og:url' in item['pagemap']['metatags'][0]:
                        metatags.url = item['pagemap']['metatags'][0]['og:url']

                    if 'og:image' in item['pagemap']['metatags'][0]:
                        metatags.image = item['pagemap']['metatags'][0]['og:image']

                    if 'og:locale' in item['pagemap']['metatags'][0]:
                        metatags.locale = item['pagemap']['metatags'][0]['og:locale']

                    if 'og:locale:alternate' in item['pagemap']['metatags'][0]:
                        metatags.locale_alternate = item['pagemap']['metatags'][0]['og:locale:alternate']
                else:
                    metatags = None
            else:
                cse_image = None
                cse_thumbnail = None
                metatags = None

            pagemap = Pagemap(cse_image=cse_image, cse_thumbnail=cse_thumbnail, metatags=metatags)

            search_item = Item()
            if 'kind' in item:
                search_item.kind = item['kind']

            if 'title' in item:
                search_item.title = item['title']

            if 'htmlTitle' in item:
                search_item.html_title = item['htmlTitle']

            if 'link' in item:
                search_item.link = item['link']

            if 'displayLink' in item:
                search_item.display_link = item['displayLink']

            if 'snippet' in item:
                search_item.snippet = item['snippet']

            if 'htmlSnippet' in item:
                search_item.html_snippet = item['htmlSnippet']

            if 'cacheId' in item:
                search_item.cache_id = item['cacheId']

            if 'formattedUrl' in item:
                search_item.formatted_url = item['formattedUrl']

            if 'htmlFormattedUrl' in item:
                search_item.html_formatted_url = item['htmlFormattedUrl']

            search_item.pagemap = pagemap

            search_result.items.append(search_item)

    return search_result


class SearchResult(object):
    def __init__(self, search_information=None, request=None, next_page=None):
        """
        :param search_information: SearchInformation
        :param request: Request
        :param next_page: NextPage
        :return:
        """

        self.search_information = search_information
        self.request = request
        self.next_page = next_page
        self.items = []

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class SearchInformation(object):
    def __init__(self, search_time=0, formatted_search_time=0, total_results=0, formatted_total_results=0):
        """
        :param search_time: integer
        :param formatted_search_time: integer
        :param total_results: integer
        :param formatted_total_results: integer
        :return:
        """
        self.search_time = search_time
        self.formatted_search_time = formatted_search_time
        self.total_results = total_results
        self.formatted_total_results = formatted_total_results


class Query(object):
    def __init__(self,
                 title='',
                 total_results=0,
                 search_terms='',
                 count=0,
                 start_index=1,
                 input_encoding='utf8',
                 output_encoding='utf8',
                 safe='off',
                 cx=''):
        """
        :param title: string
        :param total_results: integer
        :param search_terms: string
        :param count: integer
        :param start_index: integer
        :param input_encoding: string
        :param output_encoding: string
        :param safe: string
        :param cx: string
        :return:
        """

        self.title = title
        self.total_results = total_results
        self.search_terms = search_terms
        self.count = count
        self.start_index = start_index
        self.input_encoding = input_encoding
        self.output_encoding = output_encoding
        self.safe = safe
        self.cx = cx


class Request(Query):
    pass


class NextPage(Query):
    pass


class Item(object):
    def __init__(self,
                 kind='',
                 title='',
                 html_title='',
                 link='',
                 display_link='',
                 snippet='',
                 html_snippet='',
                 cache_id='',
                 formatted_url='',
                 html_formatted_url='',
                 pagemap=None):
        """
        :param kind: string
        :param title: string
        :param html_title: string
        :param link: string
        :param display_link: string
        :param snippet: string
        :param html_snippet: string
        :param cache_id: string
        :param formatted_url: string
        :param html_formatted_url: string
        :param pagemap: Pagemap
        :return:
        """

        self.kind = kind
        self.title = title
        self.html_title = html_title
        self.link = link
        self.display_link = display_link
        self.snippet = snippet
        self.html_snippet = html_snippet
        self.cache_id = cache_id
        self.formatted_url = formatted_url
        self.html_formatted_url = html_formatted_url
        self.pagemap = pagemap

    def __str__(self):
        return self.title


class Pagemap(object):
    def __init__(self, cse_image=None, cse_thumbnail=None, metatags=None):
        """
        :param cse_image: CseImage
        :param cse_thumbnail: CseThumbnail
        :param metatags: Metatags
        :return:
        """

        self.cse_image = cse_image
        self.cse_thumbnail = cse_thumbnail
        self.metatags = metatags


class CseImage(object):
    def __init__(self, src=''):
        """
        :param src: string
        :return:
        """

        self.src = src


class CseThumbnail(object):
    def __init__(self, width=0, height=0, src=''):
        """
        :param width: integer
        :param height: integer
        :param src: string
        :return:
        """

        self.width = width
        self.height = height
        self.src = src


class Metatags(object):
    def __init__(self, referrer='', site_name='', url='', image='', locale='', locale_alternate=''):
        """
        :param referrer: string
        :param site_name: string
        :param url: string
        :param image: string
        :param locale: string
        :param locale_alternate: string
        :return:
        """

        self.referrer = referrer
        self.site_name = site_name
        self.url = url
        self.image = image
        self.locale = locale
        self.locale_alternate = locale_alternate