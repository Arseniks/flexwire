from django.db import models
from django.db.models import Prefetch
from django.db.models import Q


class TeamManager(models.Manager):
    def teams(self, user_id):
        from teams.models import Team

        return (
            self.get_queryset()
            .select_related(Team.creator.field.name)
            .filter(
                Q(roleteams__members__user_id=user_id)
                | Q(is_published=True)
                | Q(creator_id=user_id)
            )
            .distinct()
        )

    def get_team_list(self, user_id):
        from teams.models import Team
        from users.models import CustomUser
        from users.models import Language
        from users.models import Technology

        return (
            self.teams(user_id)
            .prefetch_related(
                Prefetch(Team.language.field.name),
                Prefetch(Team.technologies.field.name),
            )
            .select_related(Team.creator.field.name)
            .only(
                f'{Team.technologies.field.name}__'
                f'{Technology.technology.field.name}',
                f'{Team.language.field.name}__'
                f'{Language.language.field.name}',
                Team.title.field.name,
                Team.description.field.name,
                Team.image.field.name,
                f'{Team.creator.field.name}'
                f'__{CustomUser.username.field.name}',
            )
        )

    def get_team_by_pk(self, user_id, team_pk):
        from teams.models import Team
        from users.models import CustomUser

        return (
            self.teams(user_id)
            .filter(pk=team_pk)
            .select_related(Team.creator.field.name)
            .only(
                Team.title.field.name,
                Team.description.field.name,
                Team.image.field.name,
                Team.presentation.field.name,
                Team.is_published.field.name,
                f'{Team.creator.field.name}'
                f'__{CustomUser.username.field.name}',
            )
        )


class RoleTeamManager(models.Manager):
    def get_vacancies(self, team_id):
        from teams.models import RoleTeam

        return (
            self.get_queryset()
            .filter(team_id=team_id, members=None)
            .select_related(RoleTeam.role_default.field.name)
            .only(RoleTeam.role_default.field.name, RoleTeam.team.field.name)
        )


class MemberManager(models.Manager):
    def get_members(self, team_id):
        from teams.models import Member
        from teams.models import RoleTeam
        from users.models import CustomUser

        return (
            self.get_queryset()
            .filter(role_team__team_id=team_id)
            .select_related(
                f'{Member.role_team.field.name}__'
                f'{RoleTeam.role_default.field.name}',
                Member.user.field.name,
            )
            .only(
                f'{Member.role_team.field.name}__'
                f'{RoleTeam.role_default.field.name}',
                f'{Member.user.field.name}__{CustomUser.username.field.name}',
                f'{Member.user.field.name}__{CustomUser.image.field.name}',
            )
        )


class PendingManager(models.Manager):
    def get_pendings(self, team_id):
        from teams.models import Pending
        from teams.models import RoleTeam
        from users.models import CustomUser

        return (
            self.get_queryset()
            .filter(role_team__team_id=team_id, role_team__members=None)
            .select_related(
                f'{Pending.role_team.field.name}'
                f'__{RoleTeam.role_default.field.name}'
            )
            .only(
                f'{Pending.role_team.field.name}__'
                f'{RoleTeam.role_default.field.name}',
                f'{Pending.user.field.name}__{CustomUser.username.field.name}',
                f'{Pending.user.field.name}__{CustomUser.image.field.name}',
            )
        )
