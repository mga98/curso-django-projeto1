from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Category, Recipe
from utils.pagination import make_pagination


import os


PER_PAGE = int(os.environ.get('PER_PAGE', 6))  # Used to set a maximum number of recipes in each page.


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)

    return render(request, 'recipes/pages/recipe.html', context={
            'recipe': recipe,
            'is_detail_page': True
        })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{recipes[0].category.name} - Categorias',
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |  # The pipe | is used to put an "OR" between the filters instead of the "AND".
            Q(description__icontains=search_term)
        ),
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for "{search_term}"',
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'aditional_url_query': f'&q={search_term}'
    })
