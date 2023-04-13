import django.urls

import teams.views

app_name = 'teams'

urlpatterns = [
    django.urls.path('', teams.views.TeamsList.as_view(), name='teams_list'),
    django.urls.path(
        '<int:pk>/', teams.views.TeamDetail.as_view(), name='team_detail'
    ),
    django.urls.path(
        'create_pending/<int:pk>/',
        teams.views.CreatePending.as_view(),
        name='create_pending',
    ),
    django.urls.path(
        'remove_member/<int:pk>/',
        teams.views.RemoveMember.as_view(),
        name='remove_member',
    ),
    django.urls.path(
        'accept_pending/<int:pk>/',
        teams.views.AcceptPending.as_view(),
        name='accept_pending',
    ),
    django.urls.path(
        'reject_pending/<int:pk>/',
        teams.views.RejectPending.as_view(),
        name='reject_pending',
    ),
    django.urls.path(
        'create_team/',
        teams.views.CreateTeam.as_view(),
        name='create_team',
    ),

]
