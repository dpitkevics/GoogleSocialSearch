from django.shortcuts import render

from Search.forms import SearchForm
from Search.lib import search
from Search.lib import suggestions
from Search.lib.pagination import Pagination


def index(request):
    suggestions.retrieve_suggestions('latvia')
    if 'query' in request.GET:
        form = SearchForm(request.GET)

        if 'p' in request.GET:
            current_page = int(request.GET['p'])
        else:
            current_page = 1

        search_offset = 1 + ((current_page - 1) * 10)

        search_result = search.do_search(request.GET['query'], search_offset)
        if search_result is not None:
            total_search_results = min(int(search_result.search_information.total_results), search.MAX_TOTAL_LOAD)

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
