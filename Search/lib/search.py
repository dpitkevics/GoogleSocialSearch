import requests
import json
from urllib.parse import quote

from GoogleSocialSearch import settings


def do_search(query):
    data = requests.get("https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s" % (
        settings.API_KEY,
        settings.API_SEARCH_CX,
        quote(query)
    ))
    search_results = json.loads(data.text)

    search_items = []
    for item in search_results['items']:
        cse_image = CseImage(src=item['pagemap']['cse_image'][0]['src'])
        cse_thumbnail = CseThumbnail(width=item['pagemap']['cse_thumbnail'][0]['width'],
                                     height=item['pagemap']['cse_thumbnail'][0]['height'],
                                     src=item['pagemap']['cse_thumbnail'][0]['src'])
        # metatags = Metatags(referrer=item['pagemap']['metatags'][0]['og:locale:a'])
        pagemap = Pagemap()

        search_item = Item(
            kind=item['kind'],
            title=item['title'],
            html_title=item['htmlTitle'],
            link=item['link'],
            display_link=item['displayLink'],
            snippet=item['snippet'],
            html_snippet=item['htmlSnippet'],
            cache_id=item['cacheId'],
            formatted_url=item['formattedUrl'],
            html_formatted_url=item['htmlFormattedUrl']
        )
        print(search_item)


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
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


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