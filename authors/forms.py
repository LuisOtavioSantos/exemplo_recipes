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
