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

    username = forms.CharField(
        label='Nome de usuário',
        error_messages={
            'required': 'Você precisa preencher o campo de usuário!',
            'min_length': 'O nome de usuário precisa ter pelo menos 4 caracteres!',
            'max_length': 'O nome de usuário pode ter no máximo 15 caracteres!'
        },
        help_text='O nome de usuário precisa ter entre 4 e 15 caracteres!',
        min_length=4,
        max_length=15,
    )

    first_name = forms.CharField(
        error_messages={'required': 'Você precisa preencher o campo de primeiro nome!'},
        label='Primeiro nome'
    )

    last_name = forms.CharField(
        error_messages={'required': 'Você precisa preencher o campo de último nome!'},
        label='Último nome'
    )

    email = forms.CharField(
        error_messages={'required': 'Você precisa preencher o campo de E-mail!'},
        label='E-mail',
        help_text='O e-mail precisa ser válido!'
    )

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(),
        validators=[strong_password],
        error_messages={'required': 'Você precisa preencher o campo da senha!'}
    )

    password2 = forms.CharField(
        label='Confirme sua senha',
        widget=forms.PasswordInput(),
        error_messages={'required': 'Você precisa repetir sua senha!'}
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

    def clean(self): 
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Verifique se as senhas são iguais!',
                code='invalid'
                )
            
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                    'Another error',
                ],
            })
