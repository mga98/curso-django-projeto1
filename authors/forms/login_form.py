from django import forms
from utils.django_forms import add_placeholder, add_attr


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Escreva seu nome de usuário')
        add_placeholder(self.fields['password'], 'Escreva sua senha')
        

    username = forms.CharField()
    add_attr(username, 'autofocus', 'autofocus')
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
