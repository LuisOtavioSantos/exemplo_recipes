from django.forms import ModelForm
from recipes.models import Recipe


class AuthorRecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'slug', 'preparation_time',
                  'preparation_time_unit', 'servings', 'servings_unit',
                  'preparation_steps', 'cover']
