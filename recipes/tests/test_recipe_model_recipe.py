from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

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
        setattr(self.recipe, field, 'A'*(max_length + 0))
        with self.assertRaises(ValidationError):  # context manager
            self.recipe.full_clean()  # Aqui a validação ocorre
