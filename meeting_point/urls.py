from django.conf.urls.static import static
from django.contrib import admin
import django.contrib.auth.urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.urls import path

import home.urls
import meeting_point
import meeting_point.settings
import meeting_point.views
import teams.urls
import users.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(home.urls)),
    path('teams/', include(teams.urls)),
    path('auth/', include(users.urls)),
    path('auth/', include(django.contrib.auth.urls)),
    path('teams/', include(teams.urls)),
]

handler404 = meeting_point.views.Custom404.as_view()


if meeting_point.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

    if hasattr(meeting_point.settings, 'MEDIA_ROOT'):
        urlpatterns += static(
            meeting_point.settings.MEDIA_URL,
            document_root=meeting_point.settings.MEDIA_ROOT,
        )
    else:
        urlpatterns += staticfiles_urlpatterns()
