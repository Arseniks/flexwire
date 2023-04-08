import django.urls

import teams.views

app_name = 'teams'

urlpatterns = [
    django.urls.path('', teams.views.TeamsList.as_view(), name='teams_list'),
]
