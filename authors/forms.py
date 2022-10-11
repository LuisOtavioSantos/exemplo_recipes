import re

from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError

#  from django.forms import Form, ModelForm


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

    username = forms.CharField(
        label='Username',
        help_text='nickname between 4 and 150 characters',
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have more than 4 characters',
            'max_length': 'Username must have 150 max length',
        },
        min_length=4, max_length=150,

    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'This field must not be empty'
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
            'required': 'This field must not be empty'
        },
        help_text=(
            'Password must have one lower case letter and one number'
        ),
        label='Type password again'
    )

    first_name = forms.CharField(
        error_messages={
            'required': 'Write your first name'
        },
        required=True,
        label='First Name'
    )

    last_name = forms.CharField(
        error_messages={
            'required': 'Write your last name'
        },
        required=True,
        label='Last Name'
    )

    email = forms.CharField(
        error_messages={
            'required': 'Email is required'
        },
        required=True,
        label='email',
        help_text=(
            'The e-mail must be valid'
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
