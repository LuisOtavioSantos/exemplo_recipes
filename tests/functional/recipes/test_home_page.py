import pytest
from selenium.webdriver.common.by import By

from .base import \
    RecipeBaseFunctionalTest  # THIS TYPE OF IMPORT IS ONLY VALID IF THE FOLDER HAS A __init__.py file inside it # noqa E501


@pytest.mark.functional_tests
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 😥', body.text)
