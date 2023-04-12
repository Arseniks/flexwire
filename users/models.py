from django.contrib.auth.models import AbstractUser
import django.db.models
from django.utils.translation import gettext_lazy as _


class Language(django.db.models.Model):
    language = django.db.models.CharField(
        max_length=255,
        verbose_name='Language',
        help_text='Specify communication language',
    )

    def __str__(self):
        return self.language


class Technology(django.db.models.Model):
    technology = django.db.models.CharField(
        max_length=255,
        verbose_name='Technology',
        help_text='Specify technology',
    )

    def __str__(self):
        return self.technology


class CustomUser(AbstractUser):
    nickname = django.db.models.CharField(
        max_length=255,
        verbose_name='Your nickname',
        help_text='Name that other users will see',
    )
    about_me = django.db.models.TextField(
        max_length=2000,
        null=True,
        blank=True,
        verbose_name='Tell more about yourself',
        help_text='Mention everything you consider to be important',
    )
    github = django.db.models.CharField(
        max_length=255,
        verbose_name='GitHub, Bitbucket or something similar',
        help_text='Specify website to allow others check your projects',
    )
    contact_data = django.db.models.CharField(
        max_length=255,
        verbose_name='Contact information',
        help_text='Let other users contact you',
    )
    city = django.db.models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Place where you live (country and city)',
        help_text='Specify your country and '
        'city to help people living nearby find you',
    )
    resume = django.db.models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True,
        verbose_name='Resume',
        help_text='Show others your resume',
    )
    languages = django.db.models.ManyToManyField(
        Language,
        verbose_name='Languages you speak',
        help_text='Specify languages you know',
    )
    technologies = django.db.models.ManyToManyField(
        Technology,
        verbose_name='Technologies you use',
        help_text='Specify your stack of technologies',
    )
    image = django.db.models.ImageField(
        'avatar', blank=True, null=True, upload_to='user_avatars/'
    )

    class EducationChoices(django.db.models.TextChoices):
        SCHOOL = 'school', _('School')
        UNIVERSITY = 'university', _('University')

    education_choose = django.db.models.CharField(
        max_length=255,
        choices=EducationChoices.choices,
        verbose_name='Education',
        help_text='Select place where you have studied',
    )
    education = django.db.models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Where have you learned?',
        help_text='University you attend or completed',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nickname = super().username
