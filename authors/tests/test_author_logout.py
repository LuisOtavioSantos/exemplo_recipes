
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(
            username='username1',
            password='Abc12345'
        )
        self.client.login(
            username='username1',
            password='Abc12345'
        )

        response = self.client.get(path=reverse(
            viewname='authors:logout'), follow=True)
        msg = 'Invalid logout request'
        self.assertIn(
            member=msg,
            container=response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_another_users(self):
        User.objects.create_user(
            username='username1',
            password='Abc12345'
        )
        self.client.login(
            username='username1',
            password='Abc12345'
        )
        url = reverse(viewname='authors:logout')
        response = self.client.post(
            path=url,
            data={'username': 'username2'},
            follow=True)

        msg = 'Invalid logout user'
        self.assertIn(
            member=msg,
            container=response.content.decode('utf-8')
        )

    def test_user_logout_succed(self):
        User.objects.create_user(
            username='username1',
            password='Abc12345'
        )
        self.client.login(
            username='username1',
            password='Abc12345'
        )
        url = reverse(viewname='authors:logout')
        response = self.client.post(
            path=url,
            data={'username': 'username1'},
            follow=True)

        msg = 'Logged out succeed! See you Later'
        self.assertIn(
            member=msg,
            container=response.content.decode('utf-8')
        )
