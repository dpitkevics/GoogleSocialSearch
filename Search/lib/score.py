import requests
from xml.dom import minidom


class Score:
    def get_page_score(self, search_item):
        self.get_alexa_page_score(search_item.link)

    def get_alexa_page_score(self, url):
        response = requests.get(url)
        print(response)