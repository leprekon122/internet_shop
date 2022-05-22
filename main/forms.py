from django.forms import ModelForm, TextInput, PasswordInput, EmailInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'username'
            }),

            'password1': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'password'
            }),


            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email'
            })
        }

