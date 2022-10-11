import re

from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError

#  from django.forms import Form, ModelForm


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} - {attr_new_val}'.strip


def change_attr(field, attr_name, attr_new_val):
    field.widget.attrs[attr_name] = f'{attr_new_val}'.strip


def change_placeholder(field, placeholder_val):
    change_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError(
            message='Password must have at least one uppercase letter,'
            'one lowercase letter and one number. The Length should be '
            'at least 8 characters', code='invalid'
        )


class FormRegister(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(field=self.fields['username'], attr_name='placeholder',
                 attr_new_val='Write username Here !!!')
        change_attr(field=self.fields['password'], attr_name='placeholder',
                    attr_new_val='Write password Here !!!')
        change_placeholder(
            field=self.fields['email'], placeholder_val='Write email Here !!!')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm your password'
            }
        ),
        error_messages={
            'required': 'This Field must not be empty'
        },
        help_text=(
            'Password must have one lower case letter and one number'
        ),
        validators=[strong_password]
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm your password'
            }
        ),
        error_messages={
            'required': 'This Field must not be empty'
        },
        help_text=(
            'Password must have one lower case letter and one number'
        )
    )

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
            'password': forms.PasswordInput(
                attrs={'placeholder': 'Type Password Here'},
            ),
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                message='Do not type %(value)s in password',
                code='invalid',
                params={'value': 'atenção'},
            )

        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'Luis' in data:
            raise ValidationError(
                message='Do not type %(value)s in first name',
                code='invalid',
                params={'value': 'Luis'}
            )

        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': ValidationError(
                    message='Password not equal',
                    code='invalid'
                ),
                'password2': ['Passwords must match', 'test']
            })
