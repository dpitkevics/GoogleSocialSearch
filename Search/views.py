from django.shortcuts import render
from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect
from django.contrib import messages

from guardian.shortcuts import assign_perm, remove_perm

import json
from urllib.parse import unquote
import html

from Search.forms import SearchForm
from Search.lib import search
from Search.lib import suggestions
from Search.lib.pagination import Pagination
from Search.models import SearchItem, SearchItemVoter, SearchItemComments, SearchItemClick
from Search.lib.exceptions import PurchaseException
from Search.lib.abstract_plugin import AbstractPlugin

from Comments.models import Comment
from Comments.forms import CommentForm

from GoogleSocialSearch.lib.network import get_client_ip
from GoogleSocialSearch.lib.integer import num_decode
from GoogleSocialSearch import settings


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

        search_plugin_instance = AbstractPlugin.load_plugin(request)
    else:
        form = SearchForm()

        search_result = None
        pagination = None
        search_plugin_instance = None


    context = {
        'form': form,
        'search_result': search_result,
        'pagination': pagination,
        'comment_form': comment_form,
        'search_plugin': search_plugin_instance
    }

    return render(request, 'Search/load_search.html', context)


def load_item(request):
    try:
        pk = num_decode(request.GET['srpk'])
        search_item = SearchItem.objects.get(pk=pk)
        comment_form = CommentForm()

        context = {
            'item': search_item,
            'comment_form': comment_form,
        }

        return render(request, 'Search/plugins/site.html', context)
    except ObjectDoesNotExist:
        pass

    messages.add_message(request, messages.ERROR, 'Item have not been found')
    return HttpResponse('')


def open_link(request, url):
    try:
        url = unquote(url)
        search_item = SearchItem.objects.get(link=url)
        search_item.add_click()

        if request.user.is_authenticated():
            search_item_clicks = SearchItemClick.objects.filter(search_item=search_item, user=request.user)
            if len(search_item_clicks) == 0:
                request.user.profile.get().add_balance(settings.BALANCE_UPDATE_AMOUNT_FOR_CLICK)

            search_item_click = SearchItemClick()
            search_item_click.search_item = search_item
            search_item_click.user = request.user
            search_item_click.save()

        return HttpResponseRedirect(search_item.link)
    except ObjectDoesNotExist:
        return HttpResponse("Incorrect URL")


def suggestion(request):
    suggestions_data = suggestions.retrieve_suggestions(request.GET['query'])
    suggestions_data = suggestions_data[1]

    return HttpResponse(json.dumps(suggestions_data), content_type='application/json')


def vote(request):
    if not request.user.is_authenticated():
        messages.add_message(request, messages.ERROR, 'You are not authenticated')
        return HttpResponse('')

    if not request.user.has_perm('Search.can_vote'):
        messages.add_message(request, messages.ERROR, "You don't have permissions to vote")
        return HttpResponse('')

    try:
        pk = num_decode(request.GET['srpk'])
        search_item = SearchItem.objects.get(pk=pk)

        try:
            SearchItemVoter.objects.get(user=request.user, search_item=search_item)

            messages.add_message(request, messages.ERROR, 'You already have voted on this item')
            return HttpResponse('')
        except ObjectDoesNotExist:
            search_item_voter = SearchItemVoter()
            search_item_voter.search_item = search_item
            search_item_voter.user = request.user

            if request.GET['type'] == 'upvote':
                vote_type = SearchItemVoter.VOTE_TYPE_UP
                search_item.add_upvote()
            elif request.GET['type'] == 'downvote':
                vote_type = SearchItemVoter.VOTE_TYPE_DOWN
                search_item.add_downvote()
            else:
                vote_type = SearchItemVoter.VOTE_TYPE_UNKNOWN

            search_item_voter.vote_type = vote_type
            search_item_voter.save()

            request.user.profile.get().add_balance(settings.BALANCE_UPDATE_AMOUNT_FOR_VOTE)

            messages.add_message(request, messages.SUCCESS, 'Vote successfully added')

            context = {
                'item': search_item
            }

            return render(request, 'Search/includes/scores.html', context)
    except ObjectDoesNotExist:
        pass

    messages.add_message(request, messages.ERROR, 'Search item is not found')
    return HttpResponse('')


def load_scores(request):
    try:
        pk = num_decode(request.GET['srpk'])
        search_item = SearchItem.objects.get(pk=pk)

        context = {
            'item': search_item
        }

        return render(request, 'Search/includes/scores.html', context)
    except ObjectDoesNotExist:
        pass

    messages.add_message(request, messages.ERROR, 'Scores for item have not been found')
    return HttpResponse('')


def add_comment(request):
    if request.user.is_authenticated() and request.method == 'POST':
        if not request.user.has_perm('Search.add_searchitemcomments'):
            messages.add_message(request, messages.ERROR, 'You have no permissions to add comments')
            return HttpResponse('')

        comment_text = request.POST['comment_text']
        if len(comment_text) > 0:
            pk = num_decode(request.POST['srpk'])

            try:
                search_item = SearchItem.objects.get(pk=pk)

                comment = Comment()
                comment.comment = html.escape(comment_text)
                comment.ip_address = get_client_ip(request)
                comment.is_public = True
                comment.is_removed = False
                comment.user = request.user
                comment.save()

                search_item_comment = SearchItemComments()
                search_item_comment.comment = comment
                search_item_comment.search_item = search_item
                search_item_comment.save()

                request.user.profile.get().add_balance(settings.BALANCE_UPDATE_AMOUNT_FOR_COMMENT)

                comment_form = CommentForm()

                context = {
                    'item': search_item,
                }

                messages.add_message(request, messages.SUCCESS, 'Comment successfully added')
                return render(request, 'Search/includes/comment_list.html', context)
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR, 'Search item is not found')
                return HttpResponse('')

    messages.add_message(request, messages.ERROR, "You are not authenticated")
    return HttpResponse('')


def purchase(request):
    if not request.user.is_authenticated():
        messages.add_message(request, messages.ERROR, 'You are not authenticated')
        return HttpResponse('')

    try:
        pk = num_decode(request.GET['srpk'])
        search_item = SearchItem.objects.get(pk=pk)

        profile = request.user.profile.get()
        balance = profile.balance

        item_price = search_item.get_price()
        comment_form = CommentForm()

        if request.GET['method'] == 'buy':
            if not request.user.has_perm('Search.can_buy'):
                raise PurchaseException('You have no permissions to buy an item')

            if search_item.owner is not None:
                raise PurchaseException('Selected item already have an owner')

            if balance < item_price:
                raise PurchaseException('Your balance exceeds item price')

            profile.remove_balance(item_price)

            search_item.owner = request.user
            search_item.save()

            assign_perm('owner', request.user, search_item)

            messages.add_message(request, messages.SUCCESS, 'Item successfully bought')
        elif request.GET['method'] == 'sell':
            if not request.user.has_perm('Search.can_sell'):
                raise PurchaseException('You have no permissions to sell an item')

            if search_item.owner != request.user:
                raise PurchaseException('You are not the owner of this item')

            search_item.owner = None
            search_item.save()

            profile.add_balance(item_price)

            remove_perm('owner', request.user, search_item)

            messages.add_message(request, messages.SUCCESS, 'Item successfully selled')

        context = {
            'item': search_item,
            'comment_form': comment_form
        }

        return render(request, 'Search/includes/search_item.html', context)
    except ObjectDoesNotExist:
        raise PurchaseException('Search item is not found')
    except PurchaseException as e:
        messages.add_message(request, messages.ERROR, e.message)
        return HttpResponse('')


def get_messages(request):
    return render(request, 'includes/messages.html', {})