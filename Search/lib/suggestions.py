import requests
import json


def retrieve_suggestions(query):
    url = "http://suggestqueries.google.com/complete/search?client=firefox&q=%s" % query

    data = requests.get(url)

    decoded_data = json.loads(data.text)

    return decoded_data