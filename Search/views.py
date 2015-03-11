from django.shortcuts import render

from Search.forms import SearchForm
from Search.lib import search


def index(request):
    if 'query' in request.GET:
        form = SearchForm(request.GET)

        search.do_search(request.GET['query'])
    else:
        form = SearchForm()

    context = {
        'form': form,
    }

    return render(request, 'Search/index.html', context)
