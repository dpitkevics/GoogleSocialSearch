import requests


def retrieve_suggestions(query):
    url = "http://suggestqueries.google.com/complete/search?client=firefox&q=%s" % query

    data = requests.get(url)

    print(data.text)