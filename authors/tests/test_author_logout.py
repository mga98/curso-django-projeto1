from django.test import TestCase

from django.contrib.auth.models import User
from django.urls import reverse

import pytest


class AuthorLogoutTest(TestCase):
    def user_register_and_login(self):
        User.objects.create_user(
            username='usertest',
            password='Testuser@1'
        )

        self.client.login(
            username='usertest',
            password='Testuser@1',
        )

    def test_user_tries_to_logout_using_GET_method(self):
        self.user_register_and_login()

        response = self.client.get(reverse('authors:logout'), follow=True)
        error_message = 'Logout não pode ser executado!'

        self.assertIn(error_message, response.content.decode('utf-8'))
    
    def test_user_tries_to_logout_another_user(self):
        self.user_register_and_login()

        response = self.client.post(
            reverse('authors:logout'),
            follow=True,
            data={
                'username': 'anotheruser',
            }
        )
        error_message = 'Usuário de logout inválido!'

        self.assertIn(error_message, response.content.decode('utf-8'))
    
    def test_user_logout_successfull(self):
        self.user_register_and_login()

        response = self.client.post(
            reverse('authors:logout'),
            follow=True,
            data={
                'username': 'usertest'
            }
        )
        successfull_message = 'Você foi deslogado.'

        self.assertIn(successfull_message, response.content.decode('utf-8'))
