from django.contrib.auth.models import AbstractUser
import django.db.models


class Language(django.db.models.Model):
    language = django.db.models.CharField(
        max_length=255,
        verbose_name='Title of language',
        help_text='Specify the title of this language',
    )

    def __str__(self):
        return self.language


class Technology(django.db.models.Model):
    technology = django.db.models.CharField(
        max_length=255,
        verbose_name='Title of technology',
        help_text='Specify the title of this technology',
    )

    def __str__(self):
        return self.technology


class CustomUser(AbstractUser):
    nickname = django.db.models.CharField(
        max_length=255,
        verbose_name='Your nickname',
        help_text='Name that other users will see',
    )
    email = django.db.models.EmailField(
        verbose_name='Your email',
        help_text='This email will be used by this '
        "website's owners and moderators to contact you",
    )
    about_me = django.db.models.TextField(
        max_length=10000,
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
    address = django.db.models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Place where you live',
        help_text='Specify your country and, if you want, '
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
        help_text='Specify technologies you know or those, '
        'which you are still learning',
    )
    image = django.db.models.ImageField(
        'avatar', blank=True, null=True, upload_to='user_avatars/'
    )

    class StudyPlaceChoices(django.db.models.TextChoices):
        SCHOOL = 'School'
        UNIVERSITY = 'University'

    study_place_choose = django.db.models.CharField(
        max_length=255,
        choices=StudyPlaceChoices.choices,
        verbose_name='Place of studies',
        help_text='Select place where you have studied',
    )
    study_place = django.db.models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Where have you learned?',
        help_text='University or courses you have completed',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nickname = super().username
