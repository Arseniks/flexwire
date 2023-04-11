from django.contrib import admin

import users.models

admin.site.register(users.models.Language)
admin.site.register(users.models.Technology)


@admin.register(users.models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        users.models.CustomUser.id.field.name,
        users.models.CustomUser.username.field.name,
        users.models.CustomUser.nickname.field.name,
        users.models.CustomUser.email.field.name,
    )
    list_display_links = (users.models.CustomUser.username.field.name,)
    filter_horizontal = (
        users.models.CustomUser.languages.field.name,
        users.models.CustomUser.technologies.field.name,
    )
    readonly_fields = (users.models.CustomUser.password.field.name,)
