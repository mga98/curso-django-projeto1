from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import ListView

from .models import Category, Recipe
from utils.pagination import make_pagination


import os


PER_PAGE = int(os.environ.get('PER_PAGE', 6))  # Used to set a maximum number of recipes in each page.


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE,
        )
        ctx.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )

        return ctx


class RecipeHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)

    return render(request, 'recipes/pages/recipe.html', context={
            'recipe': recipe,
            'is_detail_page': True
        })


class RecipeCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        category_id = self.kwargs['category_id']
        qs = get_list_or_404(
            qs.filter(
                is_published=True,
                category__id=category_id,
            )
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        category_name = ctx.get('recipes')[0].category.name
        ctx.update(
            {'title': f'{category_name}'}
        )

        return ctx


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
