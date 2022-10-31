import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .test_base import AuthorBaseFunctionalTest


class AuthorsRegisterTest(AuthorBaseFunctionalTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )

    def fill_form_data(self, form, keys):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():  # Check if the input aren't hidden.
                field.send_keys(keys)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback, email='email@email.com', input_key=' ' * 10):
        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.get_form()

        # The E-mail input requires special caracteres.
        form.find_element(By.NAME, 'email').send_keys(email)
        self.fill_form_data(form, input_key)

        callback(form)

        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Digite seu primeiro nome')
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form()  # Reload the form on page for the assertion.

            self.assertIn('Você precisa preencher o campo de primeiro nome!', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Digite seu último nome')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Você precisa preencher o campo de último nome!', form.text)
        
        self.form_field_test_with_callback(callback)

    def test_invalid_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Seu nome de usuário')
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Você precisa preencher o campo de usuário!', form.text)
        
        self.form_field_test_with_callback(callback)
    
    def test_invalid_password_error_message(self):
        def callback(form):
            password_field = self.get_by_placeholder(form, 'Digite sua senha')
            password_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Você precisa preencher o campo da senha!', form.text)

        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'Digite um e-mail válido')
            email_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Informe um endereço de email válido.', form.text)

        self.form_field_test_with_callback(callback, email='invalid_email')

    def test_passwords_dont_match(self):
        def callback(form):
            password1_field = self.get_by_placeholder(form, 'Digite sua senha')
            password2_field = self.get_by_placeholder(form, 'Repita sua senha')

            password1_field.send_keys('Password1.')
            password2_field.send_keys('Password2.')

            password2_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Verifique se as senhas são iguais!', form.text)
        
        self.form_field_test_with_callback(callback)

    def test_succesfull_user_register(self):
        def callback(form):
            first_input = self.get_by_placeholder(form, 'Seu nome de usuário')
            first_input.send_keys(Keys.ENTER)

            body = self.browser.find_element(By.TAG_NAME, 'body')

            self.assertIn('Você foi registrado com sucesso! Faça seu login.', body.text)
        
        self.form_field_test_with_callback(callback, email='', input_key='Test12@email.com')
