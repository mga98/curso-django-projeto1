import time

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .test_base import AuthorBaseFunctionalTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorBaseFunctionalTest):
    def make_login(self, usernametest='usertest', passwordtest='Usertest@1'):
        usertest = User.objects.create_user(
            username='usertest',
            password='Usertest@1',
        )

        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username_field = self.get_by_placeholder(form, 'Escreva seu nome de usuário')
        username_field.send_keys(usernametest)

        password_field = self.get_by_placeholder(form, 'Escreva sua senha')
        password_field.send_keys(passwordtest)

        form.submit()

    def test_successfull_user_login(self):
        self.make_login()

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('Você foi logado com sucesso!' , body.text)

    def test_user_login_invalid_credentials(self):
        self.make_login(usernametest='usere-rror', passwordtest='password-error')

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('Login ou senha inválidos.', body.text)

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
        )

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('Not Found', body.text)

    def test_user_login_invalid(self):
        self.make_login(usernametest='', passwordtest='')

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('Erro ao validar as informações do formulário.', body.text)
