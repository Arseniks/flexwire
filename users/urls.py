from django.urls import path
from django.contrib.auth.decorators import login_required

import users.views

app_name = 'users'

urlpatterns = [
    path('profile/<int:pk>/', users.views.Profile.as_view(), name='profile'),
    path(
        'account/',
        login_required(users.views.Account.as_view()),
        name='account'
    ),
]
