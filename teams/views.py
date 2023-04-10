from django.shortcuts import render

import teams.models


def test(request):
    context = {'teams': teams.models.Team.objects.active()}

    return render(request, 'teams/test.html', context)
