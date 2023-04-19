from django import urls

from teams import views

app_name = 'teams'

urlpatterns = [
    urls.path(
        '',
        views.TeamsList.as_view(),
        name='teams_list',
    ),
    urls.path(
        '<int:pk>/',
        views.TeamDetail.as_view(),
        name='team_detail',
    ),
    urls.path(
        'create_pending/<int:pk>/',
        views.CreatePending.as_view(),
        name='create_pending',
    ),
    urls.path(
        'remove_member/<int:pk>/',
        views.RemoveMember.as_view(),
        name='remove_member',
    ),
    urls.path(
        'accept_pending/<int:pk>/',
        views.AcceptPending.as_view(),
        name='accept_pending',
    ),
    urls.path(
        'reject_pending/<int:pk>/',
        views.RejectPending.as_view(),
        name='reject_pending',
    ),
    urls.path(
        'create_team/',
        views.CreateTeam.as_view(),
        name='create_team',
    ),
]
