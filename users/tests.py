from django.core import exceptions
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from .models import CustomUser
from .models import Language
from .models import Technology


class TestDataBaseAddUser(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.technology = Technology.objects.create(
            id=1,
            technology='technology',
        )
        cls.language = Language.objects.create(
            id=1,
            language='language',
        )

    def tearDown(self):
        CustomUser.objects.all().delete()
        Language.objects.all().delete()
        Technology.objects.all().delete()

    def test_unable_create_user_without_github(self):
        user_count = CustomUser.objects.count()

        with self.assertRaises(exceptions.ValidationError):
            self.user = CustomUser(
                id=1,
                username='username',
                email='1@gmail.com',
                nickname='nickname',
                contact_data='https://t.me/some_user',
                education_choose='university',
                education='some university',
            )

            self.user.full_clean()
            self.user.save()

            self.user.technologies.add(TestDataBaseAddUser.technology)
            self.user.languages.add(TestDataBaseAddUser.language)

            self.user.save()

        self.assertEqual(CustomUser.objects.count(), user_count)

    def test_unable_create_user_without_contact_data(self):
        user_count = CustomUser.objects.count()

        with self.assertRaises(exceptions.ValidationError):
            self.user = CustomUser(
                id=1,
                username='username',
                email='1@gmail.com',
                nickname='nickname',
                github='https://github.com/some_user',
                education_choose='university',
                education='some university',
            )

            self.user.full_clean()
            self.user.save()

            self.user.technologies.add(TestDataBaseAddUser.technology)
            self.user.languages.add(TestDataBaseAddUser.language)

            self.user.save()

        self.assertEqual(CustomUser.objects.count(), user_count)

    def test_unable_create_user_without_education_choose(self):
        user_count = CustomUser.objects.count()

        with self.assertRaises(exceptions.ValidationError):
            self.user = CustomUser(
                id=1,
                username='username',
                email='1@gmail.com',
                nickname='nickname',
                github='https://github.com/some_user',
                contact_data='https://t.me/some_user',
                education='some university',
            )

            self.user.full_clean()
            self.user.save()

            self.user.technologies.add(TestDataBaseAddUser.technology)
            self.user.languages.add(TestDataBaseAddUser.language)

            self.user.save()

        self.assertEqual(CustomUser.objects.count(), user_count)

    def test_unable_create_user_without_education(self):
        user_count = CustomUser.objects.count()

        with self.assertRaises(exceptions.ValidationError):
            self.user = CustomUser(
                id=1,
                username='username',
                email='1@gmail.com',
                nickname='nickname',
                github='https://github.com/some_user',
                contact_data='https://t.me/some_user',
                education_choose='university',
            )

            self.user.full_clean()
            self.user.save()

            self.user.technologies.add(TestDataBaseAddUser.technology)
            self.user.languages.add(TestDataBaseAddUser.language)

            self.user.save()

        self.assertEqual(CustomUser.objects.count(), user_count)

    def test_able_create_user_with_only_necessary_fields(self):
        user_count = CustomUser.objects.count()

        self.user = CustomUser(
            id=1,
            username='username',
            email='1@gmail.com',
            nickname='nickname',
            github='https://github.com/some_user',
            contact_data='https://t.me/some_user',
            education_choose='university',
            education='some university',
        )

        self.user.set_password('password')

        self.user.full_clean()
        self.user.save()

        self.user.technologies.add(TestDataBaseAddUser.technology)
        self.user.languages.add(TestDataBaseAddUser.language)

        self.user.save()

        self.assertEqual(CustomUser.objects.count(), user_count + 1)

    def test_able_create_user_with_all_fields(self):
        user_count = CustomUser.objects.count()

        self.user = CustomUser(
            id=1,
            username='username',
            email='1@gmail.com',
            nickname='nickname',
            about_me='some info',
            github='https://github.com/some_user',
            contact_data='https://t.me/some_user',
            city='Karaganda',
            resume='some_resume.pfd',
            education_choose='university',
            education='some university',
        )

        self.user.set_password('password')

        self.user.full_clean()
        self.user.save()

        self.user.technologies.add(TestDataBaseAddUser.technology)
        self.user.languages.add(TestDataBaseAddUser.language)

        self.user.save()

        self.assertEqual(CustomUser.objects.count(), user_count + 1)


class TestAccountAndProfile(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = CustomUser.objects.create(
            id=1,
            username='username',
            email='1@gmail.com',
            nickname='nickname',
            about_me='some info',
            github='https://github.com/some_user',
            contact_data='https://t.me/some_user',
            city='Karaganda',
            resume='some_resume.pfd',
            education_choose='university',
            education='some university',
        )
        cls.user2 = CustomUser.objects.create(
            id=2,
            username='username2',
            email='2@gmail.com',
            nickname='nickname2',
            github='https://github.com/some_user2',
            contact_data='https://t.me/some_user2',
            education_choose='university',
            education='some university2',
        )
        super().setUpTestData()

    def tearDown(self):
        CustomUser.objects.all().delete()

    def test_access_permitted_account(self):
        client = Client()
        client.force_login(self.user1)
        response = client.get(reverse('users:account'))
        self.assertEqual(response.status_code, 200)

    def test_access_denied_account(self):
        response = Client().get(reverse('users:account'))
        self.assertEqual(response.status_code, 302)

    def test_form_is_on_page(self):
        client = Client()
        client.force_login(self.user1)
        response = client.get(reverse('users:account'))
        self.assertContains(response, 'Your nickname:')
        self.assertContains(response, 'Tell more about yourself:')
        self.assertContains(response, 'GitHub, Bitbucket or something similar')
        self.assertContains(response, 'Contact information:')
        self.assertContains(response, 'Place where you live (country and city')
        self.assertContains(response, 'Resume:')
        self.assertContains(response, 'Languages you speak:')
        self.assertContains(response, 'Technologies you use:')
        self.assertContains(response, 'Education:')
        self.assertContains(response, 'Where have you learned?')

    def test_profile_200_big(self):
        response = Client().get(reverse('users:profile', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1@gmail.com')
        self.assertContains(response, 'nickname')
        self.assertContains(response, 'some info')
        self.assertContains(response, 'https://github.com/some_user')
        self.assertContains(response, 'https://t.me/some_user')
        self.assertContains(response, 'Karaganda')
        self.assertContains(response, 'some_resume.pfd')
        self.assertContains(response, 'university')
        self.assertContains(response, 'some university')

    def test_profile_200_small(self):
        response = Client().get(reverse('users:profile', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2@gmail.com')
        self.assertContains(response, 'nickname2')
        self.assertContains(response, 'https://github.com/some_user2')
        self.assertContains(response, 'https://t.me/some_user2')
        self.assertContains(response, 'university')
        self.assertContains(response, 'some university2')

    def test_profile_404(self):
        response = Client().get(reverse('users:profile', args=[3]))
        self.assertEqual(response.status_code, 404)
