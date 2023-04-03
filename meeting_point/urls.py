import django.contrib.auth.urls
from django.urls import include

from django.contrib import admin
import users.urls
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(users.urls)),
    path('auth/', include(django.contrib.auth.urls)),
]
