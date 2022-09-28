# from unittest import skip

from django.test import TestCase  # noqa F401
from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def tearDown(self) -> None:
        return super().tearDown()

    def test_recipe_detail_view_return_status_code_404_if_no_recipes_found(self):  # noqa E501
        response = self.client.get(
            reverse(viewname='recipes:recipe', kwargs={'id': 1000})
         )  # noqa F841
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse(viewname='recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_template_loads_the_correct_recipes(self):
        self.make_recipe(title='Test_Category')

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        self.assertIn('Test_Category', content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """ Test if recipes not published will not show """
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(viewname='recipes:recipe', kwargs={
                    'id': recipe.id})
        )
        self.assertEqual(response.status_code, 404)
