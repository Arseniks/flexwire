from django.conf import settings
from django.core import mail
from django.test import Client
from django.test import TestCase
from django.urls import reverse
import parameterized

from teams.models import Team
from teams.models import Member
from teams.models import RoleTeam
from teams.models import Role
from users.models import CustomUser
from users.models import Language
from users.models import Technology


class ViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        technology = Technology.objects.create(
            id=1,
            technology='technology',
        )
        language = Language.objects.create(
            id=1,
            language='language',
        )
        cls.user_creator = CustomUser.objects.create(
            id=1,
            username='creator',
            password='testpassword',
            email='test1@test.test',
            nickname='creator',
            contact_data='https://t.me/test1',
            education_choose='university',
            education='test university 1',
        )
        cls.user_member = CustomUser.objects.create(
            id=2,
            username='member',
            password='testpassword',
            email='test2@test.test',
            nickname='member',
            contact_data='https://t.me/test2',
            education_choose='university',
            education='test university 2',
        )
        ViewTests.user_creator.technologies.add(technology)
        ViewTests.user_creator.languages.add(language)
        ViewTests.user_member.technologies.add(technology)
        ViewTests.user_member.languages.add(language)
        team = Team.objects.create(
            title='Test title',
            description='Test description',
            language=language,
            creator=ViewTests.user_creator,
            is_published=True,
        )
        role = Role.objects.create(
            name='test role name'
        )
        role_team = RoleTeam.objects.create(
            role_default=role,
            team=team,
        )
        cls.member = Member.objects.create(
            role_team=role_team,
            user=ViewTests.user_member
        )

    def tearDown(cls):
        super().tearDown()
        CustomUser.objects.all().delete()
        Team.objects.all().delete()
        Member.objects.all().delete()
        RoleTeam.objects.all().delete()
        Role.objects.all().delete()
        Technology.objects.all().delete()
        Language.objects.all().delete()

    def test_remove_member_deleting_member(self):
        client = Client()
        client.force_login(self.user_creator)
        client.post(reverse('teams:remove_member', args=[1]))

        self.assertFalse(Member.objects.filter(pk=1).exists())

    def test_remove_member_status_code(self):
        client = Client()
        client.force_login(self.user_creator)
        response = client.post(reverse('teams:remove_member', args=[1]))

        self.assertEqual(response.status_code, 302)

    def test_remove_member_send_mail(self):
        client = Client()
        client.force_login(self.user_creator)
        client.post(reverse('teams:remove_member', args=[1]))

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'You was removed from the team')
        self.assertEqual(mail.outbox[0].body,
                         'Creator of the team Test title has made a decision to remove you from the team.\n'
                         '---\n'
                         'FLEXWIRE')
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].to, [self.user_member.email])


