# from unittest import skip

from django.test import TestCase  # noqa F401
from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def tearDown(self) -> None:
        return super().tearDown()

    def test_recipe_category_views_function_is_correct(self):
        view = resolve(
            reverse(viewname='recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_status_code_404_if_no_recipes_found(self):  # noqa E501
        response = self.client.get(
            reverse(viewname='recipes:category', kwargs={'category_id': 1000})
         )  # noqa F841
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        self.make_recipe(title='Test_Category')

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn('Test_Category', content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """ Test if recipes not published will not show """
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(viewname='recipes:category', kwargs={
                    'category_id': recipe.category.id})
        )
        self.assertEqual(response.status_code, 404)
