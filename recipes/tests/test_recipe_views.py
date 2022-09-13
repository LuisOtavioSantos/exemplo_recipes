from django.test import TestCase  # noqa F401
from django.urls import resolve, reverse
from recipes import views


class RecipeViewsTest(TestCase):
    def test_recipe_home_views_function_is_correct(self):
        # view = resolve('/')
        view = resolve(reverse(viewname='recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse(viewname='recipes:home'))  # noqa F841
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse(viewname='recipes:home'))  # noqa F841
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipe_if_no_recipes(self):
        response = self.client.get(reverse(viewname='recipes:home'))  # noqa F841
        self.assertIn('No recipes found', response.content.decode('utf-8'))

    def test_recipe_category_views_function_is_correct(self):
        view = resolve(
            reverse(viewname='recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_status_code_404_if_no_recipes_found(self):  # noqa E501
        response = self.client.get(
            reverse(viewname='recipes:category', kwargs={'category_id': 1})
         )  # noqa F841
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_return_status_code_404_if_no_recipes_found(self):  # noqa E501
        response = self.client.get(
            reverse(viewname='recipes:recipe', kwargs={'id': 1})
         )  # noqa F841
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse(viewname='recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
