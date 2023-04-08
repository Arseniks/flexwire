from django.contrib import admin

import teams.models

admin.site.register(teams.models.Team)
admin.site.register(teams.models.Role)
admin.site.register(teams.models.Member)
