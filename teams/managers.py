from django.db import models
from django.db.models import Prefetch


class TeamManager(models.Manager):
    def active(self):
        from teams.models import RoleTeam
        from teams.models import Team
        from users.models import CustomUser
        from users.models import Language
        from users.models import Technology

        return (
            self.get_queryset()
            .select_related(Team.creator.field.name)
            .filter(is_published=True)
            .prefetch_related(
                Prefetch(Team.languages.field.name),
                Prefetch(Team.technologies.field.name),
                Prefetch(
                    RoleTeam.role_default.field.name,
                    queryset=RoleTeam.objects.free(),
                ),
            )
            .only(
                Team.title.field.name,
                Team.description.field.name,
                Team.image.field.name,
                Team.presentation.field.name,
                f'{Team.creator.field.name}'
                f'__{CustomUser.username.field.name}',
                f'{Team.languages.field.name}'
                f'__{Language.language.field.name}',
                f'{Team.technologies.field.name}'
                f'__{Technology.technology.field.name}',
            )
        )


class RoleTeamManager(models.Manager):
    def free(self):
        from teams.models import RoleTeam

        return (
            self.get_queryset()
            .filter(role_default__isnull=False)
            .only(RoleTeam.role_default.field.name, RoleTeam.team.field.name)
        )
