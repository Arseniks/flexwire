# Generated by Django 3.2.17 on 2023-04-14 22:35

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(help_text='Specify communication language', max_length=255, verbose_name='Language')),
            ],
            options={
                'verbose_name': 'language',
                'verbose_name_plural': 'languages',
            },
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('technology', models.CharField(help_text='Specify technology', max_length=255, verbose_name='Technology')),
            ],
            options={
                'verbose_name': 'technology',
                'verbose_name_plural': 'technologies',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nickname', models.CharField(help_text='Name that other users will see', max_length=255, verbose_name='Your nickname')),
                ('about_me', models.TextField(blank=True, help_text='Mention everything you consider to be important', max_length=2000, null=True, verbose_name='Tell more about yourself')),
                ('github', models.CharField(help_text='Specify website to allow others check your projects', max_length=255, verbose_name='GitHub, Bitbucket or something similar')),
                ('contact_data', models.CharField(help_text='Let other users contact you', max_length=255, verbose_name='Contact information')),
                ('city', models.CharField(blank=True, help_text='Specify your country and city to help people living nearby find you', max_length=255, null=True, verbose_name='Place where you live (country and city)')),
                ('resume', models.FileField(blank=True, help_text='Show others your resume', null=True, upload_to='resumes/', verbose_name='Resume')),
                ('image', models.ImageField(blank=True, null=True, upload_to='user_avatars/', verbose_name='avatar')),
                ('education_choose', models.CharField(choices=[('school', 'School'), ('university', 'University')], help_text='Select place where you have studied', max_length=255, verbose_name='Education')),
                ('education', models.CharField(blank=True, help_text='University you attend or completed', max_length=255, null=True, verbose_name='Where have you learned?')),
                ('user_picture', models.ImageField(blank=True, help_text='Show others yourself', null=True, upload_to='user_pictures', verbose_name='User picture')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('languages', models.ManyToManyField(help_text='Specify languages you know', to='users.Language', verbose_name='Languages you speak')),
                ('technologies', models.ManyToManyField(help_text='Specify your stack of technologies', to='users.Technology', verbose_name='Technologies you use')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
