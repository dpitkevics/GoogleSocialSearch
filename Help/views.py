from django.shortcuts import render


def user_levels(request):
    context = {}

    return render(request, 'Help/user_levels.html', context)
