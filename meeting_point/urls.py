from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import users.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(users.urls)),
]

urlpatterns += static('static_dev', document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
