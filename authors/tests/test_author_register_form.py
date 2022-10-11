from authors.forms import FormRegister
from django.test import TestCase
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
