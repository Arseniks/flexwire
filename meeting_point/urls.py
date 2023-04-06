from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.urls import path

import home.urls
import meeting_point.settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(home.urls)),
]

urlpatterns += static('static_dev', document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
