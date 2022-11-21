from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import ListView, DetailView

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


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe.html'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Recipe, id=pk, is_published=True)

        return obj

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update(
            {
                'is_detail_page': True,
            }
        )

        return ctx


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


class RecipeSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_search_term(self):
        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404

        return search_term

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        search_term = self.get_search_term()
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |  # The pipe | is used like a "OR".
                Q(description__icontains=search_term)
            ),
            is_published=True,
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.get_search_term()
        ctx.update(
            {
                'page_title': f'Pesquisa por "{search_term}"',
                'aditional_url_query': f'&q={search_term}',
            }
        )

        return ctx

