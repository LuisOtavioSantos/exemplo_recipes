from django import forms
from django.contrib.auth.models import User

#  from django.forms import Form, ModelForm


class FormRegister(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        # ou
        # exclude = ['first_name']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Type a Username',
            'email': 'best email',
            'password': 'Create a password',
        }
        help_texts = {
            'email': 'The e-mail must be valid',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type First Name Here'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Type Last Name Here'
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Type Username Here'
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Type e-mail Here'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type Password Here'
            }),
        }
