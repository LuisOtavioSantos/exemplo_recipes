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

    def get_form(self):
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )
        return form

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')
        callback(form)
        return form

    def test_if_name_error_occurs(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(
                web_element=form,
                placeholder="Type your First Name Here !!!"
            )
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            # After the page atualization we need to capture form again to take the errors # noqa E501
            form = self.get_form()
            self.sleep(1)
            self.assertIn(
                member='Write your first name',
                container=form.text
            )
        self.form_field_test_with_callback(callback=callback)

    def test_if_last_name_error_occurs(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(
                web_element=form,
                placeholder="Type your Last Name Here !!!"
            )
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            # After the page atualization we need to capture form again to take the errors # noqa E501
            form = self.get_form()
            self.sleep(1)
            self.assertIn(
                member='Write your last name',
                container=form.text
            )
        self.form_field_test_with_callback(callback=callback)

    def test_if_username_error_occurs(self):
        def callback(form):
            username_name_field = self.get_by_placeholder(
                web_element=form,
                placeholder="Write username Here !!!"
            )
            username_name_field.send_keys(' ')
            username_name_field.send_keys(Keys.ENTER)
            # After the page atualization we need to capture form again to take the errors # noqa E501
            form = self.get_form()
            self.sleep(1)
            self.assertIn(
                member='This field must not be empty',
                container=form.text
            )
        self.form_field_test_with_callback(callback=callback)

    def test_if_invalid_email_error_occurs(self):
        def callback(form):
            email_name_field = self.get_by_placeholder(
                web_element=form,
                placeholder="Type your email Here !!!"
            )
            email_name_field.send_keys('email@invalid')
            email_name_field.send_keys(Keys.ENTER)
            # After the page atualization we need to capture form again to take the errors # noqa E501
            form = self.get_form()
            self.sleep(1)
            self.assertIn(
                member='The e-mail must be valid',
                container=form.text
            )
        self.form_field_test_with_callback(callback=callback)

    def test_if_passwords_do_not_match(self):
        def callback(form):
            passwords_field = self.get_by_placeholder(
                web_element=form,
                placeholder="Write password Here !!!"
            )
            passwords_field2 = self.get_by_placeholder(
                web_element=form,
                placeholder="Repeat Your Password !!!"
            )
            passwords_field.send_keys('Abc123456')
            passwords_field2.send_keys('Abc1234567')
            passwords_field2.send_keys(Keys.ENTER)
            # After the page atualization we need to capture form again to take the errors # noqa E501
            form = self.get_form()
            self.sleep(1)
            self.assertIn(
                member='Passwords must match',
                container=form.text
            )
        self.form_field_test_with_callback(callback=callback)

    def test_user_valid_data_register_success(self):
        self.browser.get(url=self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(web_element=form, placeholder="Type your First Name Here !!!").send_keys('First Name')  # noqa E501
        self.get_by_placeholder(web_element=form, placeholder="Type your Last Name Here !!!").send_keys('Last Name')  # noqa E501
        self.get_by_placeholder(web_element=form, placeholder="Write username Here !!!").send_keys('Username')  # noqa E501
        self.get_by_placeholder(web_element=form, placeholder="Type your email Here !!!").send_keys('email@gmail.com')  # noqa E501
        self.get_by_placeholder(web_element=form, placeholder="Write password Here !!!").send_keys('Abc12345')  # noqa E501
        self.get_by_placeholder(web_element=form, placeholder="Repeat Your Password !!!").send_keys('Abc12345')  # noqa E501

        # password_field = self.get_by_placeholder(web_element=form, placeholder="Repeat Your Password !!!")  # noqa E501
        # password_field.send_keys(Keys.ENTER)
        # OU
        form.submit()
        self.sleep(2)
        self.assertIn(member='User created! Login Available.',
                      container=self.browser.find_element(by=By.TAG_NAME, value='body').text)  # noqa E501
