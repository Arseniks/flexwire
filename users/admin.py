from django.contrib import admin

import users.models

admin.site.register(users.models.CustomUser)
admin.site.register(users.models.Language)
admin.site.register(users.models.Technology)
