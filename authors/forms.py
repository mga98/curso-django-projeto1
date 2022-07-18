from attr import attr, fields
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu nome de usuário')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        add_placeholder(self.fields['email'], 'Digite um e-mail válido')
        add_placeholder(self.fields['first_name'], 'Digite seu primeiro nome')
        add_placeholder(self.fields['last_name'], 'Digite seu ultimo nome')

    password = forms.PasswordInput()

    password2 = forms.CharField(
        label='Confirme sua senha',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita sua senha'
        })
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

        help_texts = {
            'email': 'O e-mail precisa ser válido!'
        }

        error_messages = {
            'username': {
                'required': 'Você precisa preencher o campo de usuário!'
            },
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Não digite "Atenção" na senha',
                code='invalid'
            )

        return data

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
