# Generated by Django 3.2.17 on 2023-04-18 13:32

import ckeditor.fields
from django.conf import settings
from django.db import migrations
from django.db import models
import django.db.models.deletion

import teams.models


class Migration(migrations.Migration):
    replaces = [
        ('teams', '0001_initial'),
        ('teams', '0002_initial'),
        ('teams', '0003_auto_20230416_1953'),
        ('teams', '0004_alter_team_description'),
    ]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_auto_20230416_1953'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Choose role name that you need in your project',
                        max_length=128,
                        verbose_name='name',
                    ),
                ),
            ],
            options={
                'verbose_name': 'role',
                'verbose_name_plural': 'roles',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'title',
                    models.CharField(
                        help_text='Write title of your project',
                        max_length=64,
                        verbose_name='title',
                    ),
                ),
                (
                    'description',
                    ckeditor.fields.RichTextField(
                        help_text='Write description of your project',
                        verbose_name='description',
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        blank=True,
                        help_text='Load image of your project',
                        null=True,
                        upload_to=teams.models.Team.get_upload_image,
                        verbose_name='image',
                    ),
                ),
                (
                    'presentation',
                    models.FileField(
                        blank=True,
                        help_text='Load presentation of your project',
                        null=True,
                        upload_to=teams.models.Team.get_upload_presentation,
                        verbose_name='presentation',
                    ),
                ),
                ('is_published', models.BooleanField(default=True)),
                (
                    'creator',
                    models.ForeignKey(
                        help_text='Person who came up with this idea of project',
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'language',
                    models.ForeignKey(
                        help_text='Specify team language',
                        on_delete=django.db.models.deletion.CASCADE,
                        to='users.language',
                    ),
                ),
                (
                    'technologies',
                    models.ManyToManyField(
                        help_text='Specify technologies your team use',
                        to='users.Technology',
                        verbose_name='technologies your team use',
                    ),
                ),
            ],
            options={
                'verbose_name': 'team',
                'verbose_name_plural': 'teams',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='RoleTeam',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'role_default',
                    models.ForeignKey(
                        help_text='Role from standard list',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='roles',
                        to='teams.role',
                    ),
                ),
                (
                    'team',
                    models.ForeignKey(
                        help_text='Choose  your teammate',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='roleteams',
                        to='teams.team',
                    ),
                ),
            ],
            options={
                'verbose_name': 'role in team',
                'verbose_name_plural': 'roles in team',
            },
        ),
        migrations.CreateModel(
            name='Pending',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'role_team',
                    models.ForeignKey(
                        help_text='Choose role that you want to be',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='pendings',
                        to='teams.roleteam',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        help_text='User for this pending',
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'verbose_name': 'pending',
                'verbose_name_plural': 'pending list',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'role_team',
                    models.ForeignKey(
                        help_text='Choose roles in your project',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='members',
                        to='teams.roleteam',
                    ),
                ),
                (
                    'user',
                    models.OneToOneField(
                        help_text='User for this role',
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'verbose_name': 'member',
                'verbose_name_plural': 'members',
            },
        ),
    ]