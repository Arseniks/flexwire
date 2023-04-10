from django.urls import path

import teams.views

app_name = 'teams'

urlpatterns = [
    path('', teams.views.test, name='test'),
]
