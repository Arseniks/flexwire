from django.db import models
from django.db.models import Prefetch

from teams.models import RoleTeam
from teams.models import Team
from users.models import CustomUser
from users.models import Language
from users.models import Technology


class TeamManager(models.Manager):
    def active(self):
        return (
            self.get_queryset()
            .select_related(Team.creator.field.namee)
            .filter(is_published=True)
            .prefetch_related(
                Prefetch(Team.languages.field.name),
                Prefetch(Team.technologies.field.name),
                Prefetch(
                    RoleTeam.role_default.field.name,
                    queryset=RoleTeam.objects.filter(team=Team.title),
                ),
            )
            .only(
                Team.title.field.name,
                Team.description.field.name,
                Team.image.field.name,
                Team.presentation.field.name,
                f'{Team.creator.field.name}__{CustomUser.username.field.name}',
                f'{Team.languages.related.name}__{Language.language.field.name}',
                f'{Team.technologies.related.name}__{Technology.technology.field.name}',
            )
        )
