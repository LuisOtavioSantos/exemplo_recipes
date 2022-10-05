import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from utils.pagination import make_pagination

from recipes.models import Recipe

# from utils.recipes.factory import make_recipe  # noqa F401
PER_PAGES = os.environ.get('PER_PAGE', 6)


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('id')
    # paginator recebe as receitas filtradas no model Recipes
    page_obj, pagination_range = make_pagination(
        request=request, recipes=recipes, perpage=PER_PAGES)
    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )
    page_obj, pagination_range = make_pagination(
        request=request, recipes=recipes, perpage=PER_PAGES)
    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'title': f'{page_obj[0].category.name} - Category | ',
        'pagination_range': pagination_range,
    })


def recipe(request, id):
    # recipe = Recipe.objects.filter(
    #     pk=id,
    #     is_published=True,
    # ).order_by('-id').first()

    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()
    # OR no django
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('id')
    page_obj, pagination_range = make_pagination(
        request=request, recipes=recipes, perpage=PER_PAGES)
    return render(request=request, template_name='recipes/pages/search.html',
                  context={
                      'page_title': f'Search for "{search_term}"',
                      'search_term': search_term,
                      'recipes': page_obj,
                      'pagination_range': pagination_range,
                      'additional_query': f'&q={search_term}'
                  })


# def search(request):
#     search_term = request.GET.get('q', '').strip()
#     if not search_term:
#         raise Http404()
#     # OR no django
#     recipes = Recipe.objects.filter(
#         Q(title__icontains=search_term) |
#         Q(description__icontains=search_term),
#     )
#     recipes = recipes.order_by('id')
#     recipes = recipes.filter(is_published=True)
#     return render(request=request, template_name='recipes/pages/search.html',
#                   context={
#                       'page_title': f'Search for "{search_term}"',
#                       'recipes': recipes,
#                   })
