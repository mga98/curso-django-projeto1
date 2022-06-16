from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search'))
        
        self.assertIs(view.func, views.search)

    def test_recipe_search_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=Teste')
        
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_view_raises_404_if_no_correct_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_search_term_is_on_page_title_and_scaped(self):
        url = reverse('recipes:search') + '?q=<test_term>'
        response = self.client.get(url)
        content = response.content.decode('utf-8')

        self.assertIn('Search for &quot;&lt;test_term&gt;&quot;', content)
