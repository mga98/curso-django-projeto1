from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:index'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200(self):
        response = self.client.get(reverse('recipes:index'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:index'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:index'))
        self.assertIn(
            '<h1>No recipes found here.</h1>',
            response.content.decode('utf-8'),
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:index'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:index'))
        response_context_recipes = response.context['recipes']

        self.assertEqual(len(response_context_recipes), 0)

    def test_recipe_home_template_is_paginated(self):
        self.make_recipe_in_batch(8)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:index'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 2)

    def test_invalid_page_query_uses_page_one(self):
        url = reverse('recipes:index')
        response = self.client.get(url + '?page=1A')
        ...
        self.assertEqual(response.context['recipes'].number, 1)
