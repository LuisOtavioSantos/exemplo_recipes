from django import forms
from utils.django_forms import change_placeholder


class FormLogin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        change_placeholder(
            field=self.fields['username'],
            placeholder_val='Type your username')
        change_placeholder(
            field=self.fields['password'],
            placeholder_val='Type your password')
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
