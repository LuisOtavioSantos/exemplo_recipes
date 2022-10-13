import re

from django.forms import ValidationError


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
            'at least 8 characters',
            code='invalid'
        )
