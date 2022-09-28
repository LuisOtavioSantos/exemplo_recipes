# from unittest import skip

from django.test import TestCase  # noqa F401
from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def tearDown(self) -> None:
        return super().tearDown()

    def test_recipe_search_uses_correct_view_function(self):
        url = reverse(viewname='recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        url = reverse(viewname='recipes:search') + '?q=test'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        # o teste passa pois a view retorna uma query/search_term none por padrão # noqa E501
        url = reverse(viewname='recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse(viewname='recipes:search') + '?q=<Test>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Test&gt;&quot;',
            response.content.decode('utf-8')
        )
