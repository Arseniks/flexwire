from django.test import Client
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from users.models import CustomUser


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

    @parameterized.expand(
        ('Your nickname:',),
        ('Tell more about yourself:',),
        ('GitHub, Bitbucket or something similar',),
        ('Contact information:',),
        ('Place where you live (country and city)',),
        ('Resume:',),
        ('Languages you speak:',),
        ('Technologies you use:',),
        ('Education:',),
        ('Where have you learned?',),
    )
    def test_form_is_on_page(self, content):
        client = Client()
        client.force_login(self.user1)
        response = client.get(reverse('users:account'))
        self.assertContains(response, content)

    @parameterized.expand(
        ('1@gmail.com',),
        ('nickname',),
        ('some info',),
        ('https://github.com/some_user',),
        ('https://t.me/some_user',),
        ('Karaganda',),
        ('some_resume.pfd',),
        ('university',),
        ('some university',),
    )
    def test_profile_200_big(self, content):
        response = Client().get(reverse('users:profile', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, content)

    @parameterized.expand(
        ('2@gmail.com',),
        ('nickname2',),
        ('https://github.com/some_user2',),
        ('https://t.me/some_user2',),
        ('university',),
        ('some university2',),
    )
    def test_profile_200_small(self, content):
        response = Client().get(reverse('users:profile', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, content)

    def test_profile_404(self):
        response = Client().get(reverse('users:profile', args=[3]))
        self.assertEqual(response.status_code, 404)
