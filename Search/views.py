from django.shortcuts import render
from django.http.response import HttpResponse

import json

from Search.forms import SearchForm
from Search.lib import search
from Search.lib import suggestions
from Search.lib.pagination import Pagination


def index(request):
    if 'query' in request.GET:
        form = SearchForm(request.GET)

        if 'p' in request.GET:
            current_page = int(request.GET['p'])
        else:
            current_page = 1

        search_offset = 1 + ((current_page - 1) * 10)

        search_result = search.do_search(request.GET['query'], search_offset)

        if search_result is not None:
            total_search_results = min(int(search_result.total_results), search.MAX_TOTAL_LOAD)

            pagination = Pagination(request, total_search_results, current_page)
        else:
            pagination = None
    else:
        form = SearchForm()

        search_result = None
        pagination = None

    context = {
        'form': form,
        'search_result': search_result,
        'pagination': pagination
    }

    return render(request, 'Search/index.html', context)


def open_link(request):
    pass


def suggestion(request):
    suggestions_data = suggestions.retrieve_suggestions(request.GET['query'])
    suggestions_data = suggestions_data[1]

    return HttpResponse(json.dumps(suggestions_data), content_type='application/json')
