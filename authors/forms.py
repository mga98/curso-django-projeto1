from attr import attr, fields
from django import forms
from django.contrib.auth.models import User


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

    password_confirm = forms.CharField(
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
