from django.contrib import admin

import teams.models


admin.site.register(teams.models.Role)
admin.site.register(teams.models.RoleTeam)


@admin.register(teams.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        teams.models.Team.id.field.name,
        teams.models.Team.title.field.name,
        teams.models.Team.creator.field.name,
        teams.models.Team.is_published.field.name,
    )
    list_display_links = (teams.models.Team.title.field.name,)
    list_editable = (teams.models.Team.is_published.field.name,)
    filter_horizontal = (
        teams.models.Team.languages.field.name,
        teams.models.Team.technologies.field.name,
    )


@admin.register(teams.models.Member)
class MembersAdmin(admin.ModelAdmin):
    list_display = (
        teams.models.Member.id.field.name,
        teams.models.Member.role_team.field.name,
        teams.models.Member.user.field.name,
    )
    list_display_links = (
        teams.models.Member.id.field.name,
        teams.models.Member.role_team.field.name,
    )


@admin.register(teams.models.Pending)
class PendingAdmin(admin.ModelAdmin):
    list_display = (
        teams.models.Pending.id.field.name,
        teams.models.Pending.role_team.field.name,
        teams.models.Pending.user.field.name,
    )
    list_display_links = (
        teams.models.Pending.id.field.name,
        teams.models.Pending.role_team.field.name,
    )
