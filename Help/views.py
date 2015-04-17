from django.shortcuts import render


def user_levels(request):
    context = {}

    return render(request, 'Help/user_levels.html', context)


def set_as_homepage(request):
    context = {}

    return render(request, 'Help/set_as_homepage.html', context)


def set_as_default_search_engine(request):
    context = {}

    return render(request, 'Help/set_as_default_search_engine.html', context)
