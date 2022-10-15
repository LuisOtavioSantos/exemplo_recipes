import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from tests.functional.authors.base import AuthorBaseTest


@pytest.mark.functional_tests
class AuthorsLoginTest(AuthorBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        user = User.objects.create_user(
            username='johndoe', password='Abc12345')

        # user opens the login page
        url = reverse(viewname='authors:login')
        self.browser.get(self.live_server_url + url)

        # user see the main form
        form = self.browser.find_element(by=By.CLASS_NAME, value='main-form')
        username_field = self.get_by_placeholder(
            web_element=form, placeholder='Type your username')
        password_field = self.get_by_placeholder(
            web_element=form, placeholder='Type your password')

        # user type her/his info
        username_field.send_keys(user.username)
        password_field.send_keys('Abc12345')
        form.submit()
        self.sleep()
        # assertion
        self.assertIn(member=f'You Are Logged As {user.username}',  # noqa E501
        container=self.browser.find_element(by=By.TAG_NAME, value='body').text)  # noqa E501
        # end test
