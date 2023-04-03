
from django.urls import path

import home.views

app_name = 'home'

urlpatterns = [
    path('landing/', home.views.Landing.as_view(), name='landing'),
    # path('about/', views.HomeView.as_view(), name='home'),
]
