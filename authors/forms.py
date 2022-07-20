from attr import attr, fields
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Sua senha deve ter no mínimo uma letra maiúscula, '
            'uma letra minúsucla e um número. '
            'E deve ter no mínimo 8 carateres.'
        ))


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu nome de usuário')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        add_placeholder(self.fields['password2'], 'Repita sua senha')
        add_placeholder(self.fields['email'], 'Digite um e-mail válido')
        add_placeholder(self.fields['first_name'], 'Digite seu primeiro nome')
        add_placeholder(self.fields['last_name'], 'Digite seu último nome')

    password = forms.CharField(
        label='Senha',
        required=True,
        widget=forms.PasswordInput(),
        validators=[strong_password],
    )

    password2 = forms.CharField(
        label='Confirme sua senha',
        required=True,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
        ]

        labels = {
            'first_name': 'Primeiro nome',
            'last_name': 'Último nome',
            'username': 'Nome de usuário',
            'email': 'E-mail'
        }

        help_texts = {
            'email': 'O e-mail precisa ser válido!'
        }

        error_messages = {
            'username': {
                'required': 'Você precisa preencher o campo de usuário!'
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Verifique se as senhas são iguais',
                code='invalid'
                )
            
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                    'Another error',
                ],
            })
