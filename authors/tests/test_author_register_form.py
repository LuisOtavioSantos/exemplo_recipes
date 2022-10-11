from unittest import TestCase

from authors.forms import FormRegister
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('username', 'Write username Here !!!'),
        ('email', 'Type your email Here !!!'),
        ('first_name', 'Type your First Name Here !!!'),
        ('last_name', 'Type your Last Name Here !!!'),
        ('password', 'Write password Here !!!'),
        ('password2', 'Repeat Your Password !!!'),
    ])
    def test_fields_placeholder_is_correct(self, field, message):
        form = FormRegister()
        placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(message, placeholder)

    @parameterized.expand([
        ('email', 'The e-mail must be valid'),
        ('password', 'Password must have one lower case letter and one number'),  # noqa E501
        ('password2', 'Password must have one lower case letter and one number'),  # noqa E501
    ])
    def test_fields_help_text(self, field, message):
        form = FormRegister()
        current = form[field].field.help_text
        self.assertEqual(message, current)

    @parameterized.expand([
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('username', 'Type a Username'),
        ('email', 'best email'),
        ('password', 'Create a password'),
        ('password2', 'Type password again'),
    ])
    def test_fields_labels(self, field, message):
        form = FormRegister()
        current = form[field].field.label
        self.assertEqual(message, current)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'Abc12345678',
            'password2': 'Abc12345678',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty')
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse(viewname='authors:create')
        response = self.client.post(path=url, data=self.form_data, follow=True)  # noqa F481
        self.assertIn(msg, response.content.decode('utf-8'))
