from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.urls import path
import django_select2.urls

import feedback.urls
import home.urls

from meeting_point import settings
from meeting_point import views

import teams.urls
import users.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(home.urls)),
    path('auth/', include(users.urls)),
    path('auth/', include(urls)),
    path('select2/', include(django_select2.urls)),
    path('teams/', include(teams.urls)),
    path('feedback/', include(feedback.urls)),
]

handler404 = views.Custom404.as_view()

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

    if hasattr(settings, 'MEDIA_ROOT'):
        urlpatterns += static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        )
    else:
        urlpatterns += staticfiles_urlpatterns()
