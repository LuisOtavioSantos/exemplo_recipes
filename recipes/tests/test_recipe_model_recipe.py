from django.core.exceptions import ValidationError

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
