import django.contrib.auth.urls
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.urls import path

import users.urls
import home.urls
import meeting_point.settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(home.urls)),
    path('auth/', include(users.urls)),
    path('auth/', include(django.contrib.auth.urls)),
]

if meeting_point.settings.DEBUG:
    if hasattr(meeting_point.settings, 'MEDIA_ROOT'):
        urlpatterns += static(
            meeting_point.settings.MEDIA_URL,
            document_root=meeting_point.settings.MEDIA_ROOT
        )
    else:
        urlpatterns += staticfiles_urlpatterns()
