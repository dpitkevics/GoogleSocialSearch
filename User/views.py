from django.shortcuts import render
from django.http.response import HttpResponse

from User.lib.money import convert_to_money

def login(request):
    pass


def get_balance(request):
    if request.user.is_authenticated():
        profile = request.user.profile.get()
        balance = profile.balance
    else:
        balance = 0

    return HttpResponse(convert_to_money(balance))


def get_experience(request):
    if request.user.is_authenticated():
        return render(request, 'includes/experience_bar.html', {})

    return HttpResponse('')