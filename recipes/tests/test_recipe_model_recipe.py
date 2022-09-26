from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            # os dois ultimos campos não podem ser enviados,
            # pois queremos testá-los
            # preparation_steps_is_html=False,
            # is_published=True,
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    def test_recipe_title_raises_error_if_more_65(self):
        self.recipe.title = "A"*70
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # Aqui a validação ocorre
        # self.recipe.save()  # O Django vai salvar na base de dados
        # self.fail(self.recipe.title)

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65)
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        """ Este teste em específico não é reconhecido pelo unittest
        pois ele possui subtestes, neste caso deve-se utilizar no terminal
        o seguinte comando python manage.py test"""
        setattr(self.recipe, field, 'A'*(max_length + 1))
        with self.assertRaises(ValidationError):  # context manager
            self.recipe.full_clean()  # Aqui a validação ocorre

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_steps_is_html,
                         msg='Recipe preparation_steps_is_html is not False')

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published,
                         msg='Recipe is_published is not False')

    def test_recipe_string_representation(self):
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing Representation',
                         msg='Recipe title is not changing')
