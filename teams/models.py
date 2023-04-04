import django.db.models

import pathlib

import users.models


class Team(django.db.models.Model):
    def get_upload_image(instance, filename):
        return (
                pathlib.Path('team_files') / pathlib.Path(str(instance.pk)) /
                f'team_image.{filename.split(".")[-1]}'
        )

    def get_upload_presentation(instance, filename):
        return (
                pathlib.Path('team_files') / pathlib.Path(str(instance.pk)) /
                f'presentation.{filename.split(".")[-1]}'
        )

    title = django.db.models.CharField('', help_text='', max_length=64)
    description = django.db.models.TextField('', help_text='')
    image = django.db.models.ImageField('', help_text='',
                                        null=True, blank=True,
                                        upload_to=get_upload_image)
    presentation = django.db.models.FileField('', help_text='',
                                              null=True, blank=True,
                                              upload_to=get_upload_presentation)
    creator = django.db.models.OneToOneField(
        users.models.CustomUser,
        on_delete=django.db.models.deletion.CASCADE
    )
    languages = django.db.models.ManyToManyField(
        to=users.models.Language,
        verbose_name='Languages',
        help_text='Specify team languages',
    )
    technologies = django.db.models.ManyToManyField(
        to=users.models.Technology,
        verbose_name='Technologies your team use',
        help_text='Specify technologies your team use',
    )
    is_published = django.db.models.BooleanField(default=True)


class Role(django.db.models.Model):
    name = django.db.models.CharField('', max_length=128)


class RoleTeam(django.db.models.Model):
    role_default = django.db.models.ForeignKey(
        help_text='',
        to=Role,
        on_delete=django.db.models.deletion.CASCADE
    )
    team = django.db.models.ForeignKey(
        help_text='',
        to=Team,
        on_delete=django.db.models.deletion.CASCADE
    )


class Member(django.db.models.Model):
    role_team = django.db.models.ForeignKey(
        help_text='',
        to=RoleTeam,
        on_delete=django.db.models.deletion.CASCADE
    )
    user = django.db.models.OneToOneField(
        help_text='',
        to=users.models.CustomUser,
        on_delete=django.db.models.deletion.CASCADE
    )


class Pending(django.db.models.Model):
    role_team = django.db.models.ForeignKey(
        help_text='',
        to=RoleTeam,
        on_delete=django.db.models.deletion.CASCADE
    )
    user = django.db.models.OneToOneField(
        help_text='',
        to=users.models.CustomUser,
        on_delete=django.db.models.deletion.CASCADE,
    )
