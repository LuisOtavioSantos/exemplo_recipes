# from unittest import skip

from unittest.mock import patch

from django.test import TestCase  # noqa F401
from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def tearDown(self) -> None:
        return super().tearDown()

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

    # @skip('Skip this test') # skipa o teste
    def test_recipe_home_template_shows_no_recipe_if_no_recipes(self):
        # Recipe.objects.get(pk=1).delete()
        response = self.client.get(reverse(viewname='recipes:home'))  # noqa F841
        self.assertIn('No recipes found', response.content.decode('utf-8'))
        # self.fail('Failure')  # manda o teste falhar de propósito

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        # response.context['recipes'].first().title
        # response.context['recipes'].first().category.name
        # response.context['recipes'].first().id
        # check if one recipe exists
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """ Test if recipes not published will not show """
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf-8'))

    # @patch('recipes.views.PER_PAGES', new=3)
    def test_recipe_home_is_paginated(self):

        self.make_recipe_batch(qtd=8)

        with patch('recipes.views.PER_PAGES', new=3):
            url = reverse('recipes:home')
            response = self.client.get(url)
            # app_name = request.resolver_match.app_name
            recipes = response.context['recipes']
            paginator = recipes.paginator
            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_make_pagination_returns_1_if_wrong_page(self):
        self.make_recipe_batch(qtd=8)

        with patch('recipes.views.PER_PAGES', new=3):
            url = reverse('recipes:home') + '?page=1A'
            response = self.client.get(url)
            self.assertEqual(
                first=response.context['recipes'].number,
                second=1
            )

            url = reverse('recipes:home') + '?page=2'
            response = self.client.get(url)
            self.assertEqual(
                first=response.context['recipes'].number,
                second=2
            )
