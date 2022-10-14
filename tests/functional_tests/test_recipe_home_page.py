import os
from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from utils.browser import make_chrome_browser


class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        sleep(seconds)


class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_chrome_browser(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(by=By.TAG_NAME, value='body')
        self.assertIn('No recipes found here 😥', body.text)
