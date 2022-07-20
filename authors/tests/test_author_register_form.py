from authors.forms import RegisterForm
from django.test import TestCase
from parameterized import parameterized


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
        ('email', 'O e-mail precisa ser válido!')
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
