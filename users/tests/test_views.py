from datetime import datetime

from django.test import Client
from django.test import override_settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from users.models import CustomUser
from users.views import decode_token
from users.views import generate_token


class ViewsTests(TestCase):
    user_register_data_1 = {
        'username': 'TestUsername1',
        'nickname': 'TestNickname1',
        'github': 'https://github.com/testgithub1',
        'contact_data': 'test contact info 1',
        'email': 'test@test.test',
        'password1': 'testpassword1231',
        'password2': 'testpassword1231',
    }
    user_register_data_2 = {
        'username': 'TestUsername2',
        'nickname': 'TestNickname2',
        'github': 'https://github.com/testgithub2',
        'contact_data': 'test contact info 2',
        'email': 'test@test.test',
        'password1': 'testpassword1232',
        'password2': 'testpassword1232',
    }
    user_login_data_1 = {
        'username': 'TestUsername1',
        'password': 'testpassword1231',
    }

    def test_user_signup_context(self):
        response = Client().get(
            reverse(
                'users:signup',
            )
        )
        self.assertIn('form', response.context)

    def test_user_signup_success_redirect(self):
        response = Client().post(
            reverse('users:signup'),
            self.user_register_data_1,
            follow=True,
        )

        self.assertRedirects(response, reverse('users:login'))

    def test_user_signup_success(self):
        user_count = CustomUser.objects.count()

        Client().post(
            reverse('users:signup'),
            self.user_register_data_1,
            follow=True,
        )

        self.assertEqual(CustomUser.objects.count(), user_count + 1)

    def test_user_login_success(self):
        response = Client().post(
            reverse('users:login'),
            self.user_login_data_1,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    @override_settings(DEFAULT_USER_ACTIVITY='False')
    def test_signup_is_active_false(self):
        Client().post(
            reverse('users:signup'),
            self.user_register_data_1,
            follow=True,
        )

        user = CustomUser.objects.get(
            username=self.user_register_data_1['username']
        )

        self.assertFalse(user.is_active)

    @override_settings(DEFAULT_USER_ACTIVITY='True')
    def test_signup_is_active_true(self):
        Client().post(
            reverse('users:signup'),
            self.user_register_data_1,
            follow=True,
        )

        user = CustomUser.objects.get(
            username=self.user_register_data_1['username']
        )

        self.assertTrue(user.is_active)

    @override_settings(DEFAULT_USER_ACTIVITY='False')
    def test_user_activate_user_success(self):
        Client().post(
            reverse('users:signup'),
            self.user_register_data_1,
            follow=True,
        )

        user = CustomUser.objects.get(
            username=self.user_register_data_1['username']
        )

        Client().get(
            reverse('users:activate_user', args=(user.username,)),
            follow=True,
        )

        user = CustomUser.objects.get(
            username=self.user_register_data_1['username']
        )

        self.assertFalse(user.is_active)

    def test_generating_and_encoding_jwt_tokens(self):
        username = 'TestUsername'
        expired = 1
        current_time = datetime.now(tz=timezone.utc)

        token = generate_token(username, expired)
        is_decoding_token_correct, result_token_decoding = decode_token(token)

        self.assertTrue(is_decoding_token_correct, True)
        self.assertEqual(result_token_decoding['username'], username)
        self.assertLess(current_time.timestamp(), result_token_decoding['exp'])
        self.assertGreater(
            current_time.timestamp() + 60 * 60, result_token_decoding['exp']
        )
