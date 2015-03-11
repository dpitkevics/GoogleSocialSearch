from django.shortcuts import render

from Search.forms import SearchForm
from Search.lib import search


def index(request):
    if 'query' in request.GET:
        form = SearchForm(request.GET)

        search_result = search.do_search(request.GET['query'])
    else:
        form = SearchForm()

        search_result = None

    context = {
        'form': form,
        'search_result': search_result,
    }

    return render(request, 'Search/index.html', context)
