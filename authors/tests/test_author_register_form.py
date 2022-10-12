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
        ('username', 'nickname between 4 and 150 characters'),
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
        ('username', 'Username'),
        ('email', 'email'),
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
            'email': 'email@gmail.com',
            'password': 'Abc12345678',
            'password2': 'Abc12345678',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('email', 'Email is required'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse(viewname='authors:create')
        response = self.client.post(path=url, data=self.form_data, follow=True)  # noqa F481
        keys = response.context.keys()
        print(keys)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_is_more_than_4(self):
        self.form_data['username'] = 'chi'
        url = reverse(viewname='authors:create')
        response = self.client.post(path=url, data=self.form_data, follow=True)
        msg = 'Username must have more than 4 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
        # self.assertEqual(response.status_code, 404)

    def test_username_field_is_less_than_150(self):
        self.form_data['username'] = 'k'*151
        url = reverse(viewname='authors:create')
        response = self.client.post(path=url, data=self.form_data, follow=True)
        msg = 'Username must have 150 max length'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'k123'
        url = reverse(viewname='authors:create')
        response = self.client.post(path=url, data=self.form_data, follow=True)
        msg = ('Password must have at least one uppercase letter,'
               'one lowercase letter and one number. The Length should be '
               'at least 8 characters')
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        # teste positivo
        self.form_data['password'] = 'k@Abc123'
        url = reverse(viewname='authors:create')
        response = self.client.post(path=url, data=self.form_data, follow=True)
        # se estiver correto não vai aparecer msg de erro
        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_passwords_fields_matches(self):
        self.form_data['password'] = 'Abk12348'
        self.form_data['password2'] = 'Abk123489'
        url = reverse(viewname='authors:create')
        response = self.client.post(path=url, data=self.form_data, follow=True)
        msg = 'Password not equal'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        # teste positivo
        self.form_data['password'] = '@Abk123456'
        self.form_data['password2'] = '@Abk123456'
        url = reverse(viewname='authors:create')
        response = self.client.post(path=url, data=self.form_data, follow=True)  # noqa E401
        # # se estiver correto não vai aparecer msg de erro
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_register_create_view_returns_404_if_request_is_not_post(self):  # noqa E401
        url = reverse(viewname='authors:create')
        response = self.client.get(path=url)
        self.assertEqual(first=response.status_code, second=404)

    def test_password_confirmation_matches(self):
        url = reverse('authors:create')

        self.form_data['email'] = 'email@gmail.com'

        self.client.post(
            path=url, data=self.form_data, follow=True)

        self.form_data['email'] = 'email@gmail.com'

        response2 = self.client.post(
            path=url, data=self.form_data, follow=True)

        msg = 'User e-mail is already in use'

        self.assertIn(msg, response2.context['form'].errors.get('email'))
        self.assertIn(msg, response2.content.decode('utf-8'))
