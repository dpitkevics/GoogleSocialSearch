from django.shortcuts import render
from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect

import json
from urllib.parse import unquote

from Search.forms import SearchForm
from Search.lib import search
from Search.lib import suggestions
from Search.lib.pagination import Pagination
from Search.models import SearchItem, SearchItemVoter

from Comments.forms import CommentForm

from GoogleSocialSearch.lib.network import get_client_ip
from GoogleSocialSearch.lib.integer import num_decode


def index(request):
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    else:
        form = SearchForm()

    context = {
        'form': form,
    }

    return render(request, 'Search/index.html', context)


def load_search(request):
    comment_form = CommentForm()
    print(comment_form)

    if 'query' in request.GET:
        form = SearchForm(request.GET)

        if 'p' in request.GET:
            current_page = int(request.GET['p'])
        else:
            current_page = 1

        search_offset = 1 + ((current_page - 1) * 10)

        if request.user.is_authenticated():
            user = request.user
        else:
            user = None

        search_result = search.do_search(request.GET['query'], search_offset, get_client_ip(request), user)

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
        'pagination': pagination,
        'comment_form': comment_form,
    }

    return render(request, 'Search/load_search.html', context)


def open_link(request, url):
    try:
        url = unquote(url)
        search_item = SearchItem.objects.get(link=url)
        search_item.add_click()

        return HttpResponseRedirect(search_item.link)
    except ObjectDoesNotExist:
        return HttpResponse("Incorrect URL")


def suggestion(request):
    suggestions_data = suggestions.retrieve_suggestions(request.GET['query'])
    suggestions_data = suggestions_data[1]

    return HttpResponse(json.dumps(suggestions_data), content_type='application/json')


def vote(request):
    try:
        pk = num_decode(request.GET['srpk'])
        search_item = SearchItem.objects.get(pk=pk)

        try:
            SearchItemVoter.objects.get(user=request.user, search_item=search_item)

            return HttpResponse('You already have voted')
        except ObjectDoesNotExist:
            search_item_voter = SearchItemVoter()
            search_item_voter.search_item = search_item
            search_item_voter.user = request.user
            search_item_voter.save()

            if request.GET['type'] == 'upvote':
                search_item.add_upvote()
            elif request.GET['type'] == 'downvote':
                search_item.add_downvote()

            return HttpResponse('Vote Successful')
    except ObjectDoesNotExist:
        pass
    return HttpResponse('')