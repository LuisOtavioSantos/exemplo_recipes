import re

from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError

#  from django.forms import Form, ModelForm


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} - {attr_new_val}'.strip


def change_attr(field, attr_name, attr_new_val):
    field.widget.attrs[attr_name] = f'{attr_new_val}'


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
        change_attr(field=self.fields['username'], attr_name='placeholder',
                    attr_new_val='Write username Here !!!')
        change_attr(field=self.fields['password'], attr_name='placeholder',
                    attr_new_val='Write password Here !!!')
        change_attr(field=self.fields['password2'], attr_name='placeholder',
                    attr_new_val='Repeat Your Password !!!')
        change_placeholder(
            field=self.fields['email'], placeholder_val='Type your email Here !!!')  # noqa E501
        change_placeholder(
            field=self.fields['first_name'], placeholder_val='Type your First Name Here !!!')  # noqa E501
        change_placeholder(
            field=self.fields['last_name'], placeholder_val='Type your Last Name Here !!!')  # noqa E501

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'This Field must not be empty'
        },
        help_text=(
            'Password must have one lower case letter and one number'
        ),
        validators=[strong_password],
        label='Create a password'
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'This Field must not be empty'
        },
        help_text=(
            'Password must have one lower case letter and one number'
        ),
        label='Type password again'
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
        }
        help_texts = {
            'email': 'The e-mail must be valid',
        }

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
