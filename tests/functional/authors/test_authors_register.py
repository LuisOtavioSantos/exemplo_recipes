from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tests.functional.authors.base import AuthorBaseTest


class AuthorsRegisterTest(AuthorBaseTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]'
        )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' '*20)
        return fields

    def test_if_name_error_occurs(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        first_name_field = self.get_by_placeholder(
            web_element=form,
            placeholder="Type your First Name Here !!!"
        )
        first_name_field.send_keys(' ')
        first_name_field.send_keys(Keys.ENTER)
        # After the page atualization we need to capture form again to take the errors # noqa E501
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )
        self.sleep()
        self.assertIn(
            member='Write your first name',
            container=form.text
        )
