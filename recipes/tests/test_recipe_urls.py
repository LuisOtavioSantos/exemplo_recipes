from django.test import TestCase  # noqa F401
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_the_pytest_is_ok(self):
        print('Testes do Django')
        assert 1 == 1

    def test_recipe_home_url_is_correct(self):
        url = reverse(viewname='recipes:home')
        self.assertEqual(url, '/')

    def test_recipe_category_url_is_correct(self):
        url = reverse(viewname='recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipes_recipe_url_is_correct(self):
        url = reverse(viewname='recipes:recipe', kwargs={'id': 1})
        self.assertEqual(url, '/recipes/1/')
