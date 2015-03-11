import requests
import json
from urllib.parse import quote

from GoogleSocialSearch import settings


def do_search(query):
    """
    Executes search and returns formatted objects

    :param query: string
    :return: SearchResult
    """

    data = requests.get("https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s" % (
        settings.API_KEY,
        settings.API_SEARCH_CX,
        quote(query)
    ))

    print(data.text)

    search_results = json.loads(data.text)

    search_information = SearchInformation()
    search_information.search_time = search_results['searchInformation']['searchTime']
    search_information.formatted_search_time = search_results['searchInformation']['formattedSearchTime']
    search_information.total_results = search_results['searchInformation']['totalResults']
    search_information.formatted_total_results = search_results['searchInformation']['formattedTotalResults']

    request = Request()
    request.title = search_results['queries']['request'][0]['title']
    request.total_results = search_results['queries']['request'][0]['totalResults']
    request.search_terms = search_results['queries']['request'][0]['searchTerms']
    request.count = search_results['queries']['request'][0]['count']
    request.start_index = search_results['queries']['request'][0]['startIndex']
    request.input_encoding = search_results['queries']['request'][0]['inputEncoding']
    request.output_encoding = search_results['queries']['request'][0]['outputEncoding']
    request.safe = search_results['queries']['request'][0]['safe']
    request.cx = search_results['queries']['request'][0]['cx']

    next_page = NextPage()
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
        self.search_information = search_information
        self.request = request
        self.next_page = next_page
        self.items = []

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class SearchInformation(object):
    def __init__(self, search_time=0, formatted_search_time=0, total_results=0, formatted_total_results=0):
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
        self.cse_image = cse_image
        self.cse_thumbnail = cse_thumbnail
        self.metatags = metatags


class CseImage(object):
    def __init__(self, src=''):
        self.src = src


class CseThumbnail(object):
    def __init__(self, width=0, height=0, src=''):
        self.width = width
        self.height = height
        self.src = src


class Metatags(object):
    def __init__(self, referrer='', site_name='', url='', image='', locale='', locale_alternate=''):
        self.referrer = referrer
        self.site_name = site_name
        self.url = url
        self.image = image
        self.locale = locale
        self.locale_alternate = locale_alternate