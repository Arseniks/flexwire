import pathlib

import django.db.models

import users.models


class Team(django.db.models.Model):
    def get_upload_image(self, filename):
        return (
            pathlib.Path('team_files')
            / pathlib.Path(str(self.creator.id))
            / pathlib.Path(self.title)
            / f'team_image.{filename.split(".")[-1]}'
        )

    def get_upload_presentation(self, filename):
        return (
            pathlib.Path('team_files')
            / pathlib.Path(str(self.creator.id))
            / pathlib.Path(self.title)
            / f'presentation.{filename.split(".")[-1]}'
        )

    title = django.db.models.CharField(
        'title', help_text='Write title of your project', max_length=64
    )
    description = django.db.models.TextField(
        'description', help_text='Write description of your project'
    )
    image = django.db.models.ImageField(
        'image',
        help_text='Load image of your project',
        null=True,
        blank=True,
        upload_to=get_upload_image,
    )
    presentation = django.db.models.FileField(
        'presentation',
        help_text='Load presentation of your project',
        null=True,
        blank=True,
        upload_to=get_upload_presentation,
    )
    creator = django.db.models.ForeignKey(
        users.models.CustomUser,
        help_text='Person who came up with this idea of project',
        on_delete=django.db.models.deletion.CASCADE,
    )
    languages = django.db.models.ManyToManyField(
        users.models.Language,
        help_text='Specify team languages',
    )
    technologies = django.db.models.ManyToManyField(
        users.models.Technology,
        verbose_name='Technologies your team use',
        help_text='Specify technologies your team use',
    )
    is_published = django.db.models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'team'
        verbose_name_plural = 'teams'


class Role(django.db.models.Model):
    name = django.db.models.CharField(
        'name',
        help_text='Choose role name that you need in your project',
        max_length=128,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'role'
        verbose_name_plural = 'roles'


class RoleTeam(django.db.models.Model):
    role_default = django.db.models.ForeignKey(
        Role,
        help_text='Role from standard list',
        on_delete=django.db.models.deletion.CASCADE,
    )
    team = django.db.models.ForeignKey(
        Team,
        help_text='Choose your teammate',
        on_delete=django.db.models.deletion.CASCADE,
    )

    def __str__(self):
        return f'{self.role_default.name} in team {self.team.title}'

    class Meta:
        verbose_name = 'role in team'
        verbose_name_plural = 'roles in team'


class Member(django.db.models.Model):
    role_team = django.db.models.ForeignKey(
        RoleTeam,
        help_text='Choose roles in your project',
        on_delete=django.db.models.deletion.CASCADE,
    )
    user = django.db.models.OneToOneField(
        users.models.CustomUser,
        help_text='User for this role',
        on_delete=django.db.models.deletion.CASCADE,
    )

    def __str__(self):
        return self.role_team.role_default.name

    class Meta:
        verbose_name = 'member'
        verbose_name_plural = 'members'


class Pending(django.db.models.Model):
    role_team = django.db.models.ForeignKey(
        RoleTeam,
        help_text='Choose role that you want to be',
        on_delete=django.db.models.deletion.CASCADE,
    )
    user = django.db.models.OneToOneField(
        users.models.CustomUser,
        help_text='User for this pending',
        on_delete=django.db.models.deletion.CASCADE,
    )

    def __str__(self):
        return self.role_team.role_default.name

    class Meta:
        verbose_name = 'pending'
        verbose_name_plural = 'pending list'
