from unittest import TestCase
from django.urls import reverse
from authors.forms import RegisterForm
from parameterized import parameterized
from django.test import TestCase as DjangoTestCase


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Seu nome de usuário'),
        ('password', 'Digite sua senha'),
        ('password2', 'Repita sua senha'),
        ('email', 'Digite um e-mail válido'),
        ('first_name', 'Digite seu primeiro nome'),
        ('last_name', 'Digite seu último nome'),
    ])
    def test_placeholder_fields_are_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('email', 'O e-mail precisa ser válido!'),
        ('username', 'O nome de usuário precisa ter entre 4 e 15 caracteres!')
    ])
    def test_help_texts_fields_are_correct(self, field, help_text):
        form = RegisterForm()
        current_help_text = form[field].field.help_text
        self.assertEqual(help_text, current_help_text)

    @parameterized.expand([
        ('first_name', 'Primeiro nome'),
        ('last_name', 'Último nome'),
        ('username', 'Nome de usuário'),
        ('email', 'E-mail'),
        ('password', 'Senha'),
        ('password2', 'Confirme sua senha')
    ])
    def test_labels_fields_are_correct(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(label, current_label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'Password12.',
            'password2': 'Password12.',
        }

        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Você precisa preencher o campo de usuário!'),
        ('first_name', 'Você precisa preencher o campo de primeiro nome!'),
        ('last_name', 'Você precisa preencher o campo de último nome!'),
        ('email', 'Você precisa preencher o campo de E-mail!'),
        ('password', 'Você precisa preencher o campo da senha!'),
        ('password2', 'Você precisa repetir sua senha!'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        url = reverse('authors:register_create')
        self.form_data[field] = ''

        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_min_length(self):
        url = reverse('authors:register_create')
        self.form_data['username'] = '123'

        msg = 'O nome de usuário precisa ter pelo menos 4 caracteres!'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_max_length(self):
        url = reverse('authors:register_create')
        self.form_data['username'] = 'testmaxlengthofusername'
        
        msg = 'O nome de usuário pode ter no máximo 15 caracteres!'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_strength(self):
        url = reverse('authors:register_create')
        self.form_data['password'] = 'password'
        
        msg = 'Sua senha deve ter no mínimo uma letra maiúscula,'
        'uma letra minúsucla e um número. '
        'E deve ter no mínimo 8 carateres.'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_and_password2_are_equal(self):
        url = reverse('authors:register_create')

        self.form_data['password'] = 'Password123.'
        self.form_data['password2'] = 'Password12.'
        
        msg = 'Verifique se as senhas são iguais!'
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_send_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Este E-mail já está sendo utilizado!'
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_form_is_valid(self):
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Você foi registrado com sucesso!'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_author_created_can_login(self):
        url = reverse('authors:register_create')
        self.form_data.update({
            'username': 'testuser',
            'password': 'Testuser12.',
            'password2': 'Testuser12.',
            'email': 'testuser@email.com',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='Testuser12.'
        )

        self.assertTrue(is_authenticated)
