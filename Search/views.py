from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect, HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import datetime

from guardian.shortcuts import assign_perm, remove_perm

import json
import html

from Search.forms import SearchForm
from Search.lib import search
from Search.lib import suggestions
from Search.lib.pagination import Pagination
from Search.models import SearchItem, SearchItemVoter, SearchItemComments, SearchItemClick, SearchItemFavourite
from Search.models import SearchItemOffer, SearchItemCommentReport
from Search.lib.exceptions import PurchaseException, OfferException
from Search.lib.abstract_plugin import AbstractPlugin

from Comments.models import Comment
from Comments.forms import CommentForm

from Jooglin.lib.network import get_client_ip
from Jooglin.lib.integer import num_decode
from Jooglin import settings


def index(request):
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    else:
        form = SearchForm()

    if 'p' in request.GET:
        if 'query' in request.GET:
            url = '/?query=%s' % request.GET['query']
        else:
            url = '/'

        try:
            page = int(request.GET['p'])
        except ValueError:
            messages.add_message(request, messages.ERROR, 'Invalid page parameter')
            return HttpResponseRedirect(url)

        if page > settings.MAX_SEARCH_PAGES:
            messages.add_message(request, messages.ERROR, 'Chosen page exceeds page count')
            return HttpResponseRedirect(url)

    context = {
        'form': form,
    }

    return render(request, 'Search/index.html', context)


@login_required(login_url='/login/facebook/?next=/my-favourites/')
def my_favourites(request):
    comment_form = CommentForm()

    search_item_favourites = SearchItemFavourite.objects.filter(user=request.user)

    context = {
        'comment_form': comment_form,
        'search_item_favourites': search_item_favourites
    }

    return render(request, 'Search/my_favourites.html', context)


@login_required(login_url='/login/facebook/?next=/my-items/')
def my_items(request):
    comment_form = CommentForm()

    my_search_items = SearchItem.objects.filter(owner=request.user)

    context = {
        'comment_form': comment_form,
        'search_items': my_search_items
    }

    return render(request, 'Search/my_items.html', context)


@login_required(login_url='/login/facebook/?next=/my-offers/')
def my_offers(request):
    comment_form = CommentForm()

    my_offer_list = SearchItemOffer.objects.filter(user=request.user).order_by('-offer_date')

    search_items = SearchItem.objects.filter(owner=request.user)
    offers_to_me = SearchItemOffer.objects.filter(search_item__in=search_items, offer_status=SearchItemOffer.OFFER_STATUS_PENDING).order_by('-offer_date')

    context = {
        'comment_form': comment_form,
        'my_offers': my_offer_list,
        'offers_to_me': offers_to_me
    }

    return render(request, 'Search/my_offers.html', context)


def load_search(request):
    comment_form = CommentForm()

    if 'query' in request.GET and len(request.GET['query']) > 0:
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
        pk = num_decode(request.GET.get('srpk', False))
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


def open_link(request, pk):
    try:
        pk = num_decode(pk)
        search_item = SearchItem.objects.get(pk=pk)
        search_item.add_click()

        if request.user.is_authenticated():
            search_item_clicks = SearchItemClick.objects.filter(search_item=search_item, user=request.user)
            if len(search_item_clicks) == 0:
                request.user.profile.get().add_balance(settings.BALANCE_UPDATE_AMOUNT_FOR_CLICK)
                request.user.profile.get().add_experience(settings.EXPERIENCE_UPDATE_AMOUNT_FOR_CLICK)

            search_item_click = SearchItemClick()
            search_item_click.search_item = search_item
            search_item_click.user = request.user
            search_item_click.ip_address = get_client_ip(request)
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
            request.user.profile.get().add_experience(settings.EXPERIENCE_UPDATE_AMOUNT_FOR_VOTE)

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
                request.user.profile.get().add_experience(settings.EXPERIENCE_UPDATE_AMOUNT_FOR_COMMENT)

                comment_form = CommentForm()

                context = {
                    'item': search_item,
                }

                messages.add_message(request, messages.SUCCESS, 'Comment successfully added')
                return render(request, 'Search/includes/comment_list.html', context)
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR, 'Search item is not found')
                return HttpResponse('')
        else:
            messages.add_message(request, messages.ERROR, "Comment cannot be empty")
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
                raise PurchaseException('Item price exceeds your balance')

            profile.remove_balance(item_price)

            search_item.owner = request.user
            search_item.owner_updated_at = timezone.now()
            search_item.save()

            assign_perm('owner', request.user, search_item)

            messages.add_message(request, messages.SUCCESS, 'Item successfully bought')
        elif request.GET['method'] == 'sell':
            if not search_item.is_sell_date_valid():
                raise PurchaseException(
                    'You must own an item at least 30 days to sell it. This item will be open for selling on %s' % search_item.sell_date().strftime(
                        "%d.%m.%Y %H:%M"))

            if not request.user.has_perm('Search.can_sell'):
                raise PurchaseException('You have no permissions to sell an item')

            if search_item.owner != request.user:
                raise PurchaseException('You are not the owner of this item')

            search_item.owner = None
            search_item.owner_updated_at = datetime.now()
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


def offer(request):
    if not request.user.is_authenticated():
        messages.add_message(request, messages.ERROR, 'You are not authenticated')
        return HttpResponse('')

    try:
        pk = num_decode(request.POST['srpk'])
        search_item = SearchItem.objects.get(pk=pk)

        profile = request.user.profile.get()
        balance = profile.balance

        try:
            offered_money = float(request.POST['amount'])
        except ValueError:
            raise PurchaseException('Entered amount is invalid')

        if offered_money < 1:
            raise PurchaseException('Your offer amount should be at least 1')

        if not request.user.has_perm('Search.can_buy'):
            raise PurchaseException('You have no permissions to buy an item')

        if search_item.owner is None:
            raise PurchaseException('Selected item does not have an owner')

        if offered_money > balance:
            raise PurchaseException('Offered money exceeds Your balance')

        search_item_offer = SearchItemOffer()
        search_item_offer.search_item = search_item
        search_item_offer.user = request.user
        search_item_offer.offered_amount = offered_money
        search_item_offer.save()

        messages.add_message(request, messages.SUCCESS, 'Offer successfully made')
        return HttpResponse('')
    except IndexError:
        raise PurchaseException('Search item is not found')
    except ObjectDoesNotExist:
        raise PurchaseException('Search item is not found')
    except PurchaseException as e:
        messages.add_message(request, messages.ERROR, e.message)
        return HttpResponse('')


def offer_action(request):
    if not request.user.is_authenticated():
        messages.add_message(request, messages.ERROR, 'You are not authenticated')
        return HttpResponse('')

    try:
        pk = num_decode(request.GET['opk'])
        search_item_offer = SearchItemOffer.objects.get(pk=pk)

        if search_item_offer.user != request.user and search_item_offer.search_item.owner != request.user:
            raise OfferException('You are not allowed to manipulate this offer')

        if request.GET['method'] == 'remove':
            if search_item_offer.user != request.user:
                raise OfferException('You cannot remove offers made by other user')

            search_item_offer.delete()

            messages.add_message(request, messages.SUCCESS, 'Offer successfully removed')
            return HttpResponse('')
        elif request.GET['method'] == 'accept':
            if search_item_offer.search_item.owner != request.user:
                raise OfferException('You cannot accept other user offers')

            profile = request.user.profile.get()

            offerers_profile = search_item_offer.user.profile.get()
            offerers_balance = offerers_profile.balance
            if offerers_balance < search_item_offer.offered_amount:
                raise OfferException('Balance for user who made this offer, is now less than offered amount')

            offerers_profile.remove_balance(search_item_offer.offered_amount)
            profile.add_balance(search_item_offer.offered_amount)

            search_item = search_item_offer.search_item
            search_item.owner = search_item_offer.user
            search_item.save()

            search_item_offer.offer_status = search_item_offer.OFFER_STATUS_ACCEPTED
            search_item_offer.save()

            messages.add_message(request, messages.SUCCESS, 'Offer successfully accepted')
            return HttpResponse('')
        elif request.GET['method'] == 'decline':
            if search_item_offer.search_item.owner != request.user:
                raise OfferException('You cannot decline other user offers')

            search_item_offer.offer_status = search_item_offer.OFFER_STATUS_DECLINED
            search_item_offer.save()

            messages.add_message(request, messages.SUCCESS, 'Offer successfully declined')
            return HttpResponse('')
    except IndexError:
        raise OfferException('Offer not found')
    except ObjectDoesNotExist:
        raise OfferException('Offer not found')
    except OfferException as e:
        messages.add_message(request, messages.ERROR, e.message)
        return HttpResponse('')

    return HttpResponse('')


def get_messages(request):
    return render(request, 'includes/messages.html', {})


def favourite(request, srpk):
    pk = num_decode(srpk)

    try:
        search_item_favourite = SearchItemFavourite.objects.get(search_item_id=pk, user=request.user)
        search_item_favourite.delete()
    except ObjectDoesNotExist:
        search_item_favourite = SearchItemFavourite()
        search_item_favourite.search_item_id = pk
        search_item_favourite.user = request.user
        search_item_favourite.save()

    return HttpResponse('')


def report_comment(request, cpk):
    pk = num_decode(cpk)

    try:
        search_item_comment = SearchItemComments.objects.get(pk=pk)

        search_item_comment_report = SearchItemCommentReport()
        search_item_comment_report.search_item_comment = search_item_comment
        search_item_comment_report.save()

        messages.add_message(request, messages.SUCCESS, 'Comment successfully reported. Our administration will process this report as soon as possible.')
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, 'Comment not found')

    return HttpResponse('')


def error404(request):
    return HttpResponseNotFound(render_to_response('404.html'))