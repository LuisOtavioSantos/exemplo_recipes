from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import \
    RecipeBaseFunctionalTest  # THIS TYPE OF IMPORT IS ONLY VALID IF THE FOLDER HAS A __init__.py file inside it # noqa E501


@pytest.mark.functional_tests
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 😥', body.text)

    @patch('recipes.views.PER_PAGES', new=2)
    def test_recipe_search_can_find_correct_recipe(self):
        recipes = self.make_recipe_batch(qtd=4)
        new_title = 'Bolo de Coco'
        recipes[0].title = new_title
        recipes[0].save()
        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]')

        # search_input.send_keys('title 1')
        # search_input.send_keys(recipes[0].title)
        search_input.send_keys(new_title)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            new_title,
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        self.sleep()
