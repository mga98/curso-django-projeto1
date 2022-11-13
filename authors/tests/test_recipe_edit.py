from django.urls import reverse
from django.shortcuts import get_object_or_404

from .test_authors_base import AuthorsTestBase
from recipes.models import Recipe


class RecipeEditUnitTest(AuthorsTestBase):
    def test_recipe_edit_loads_correct_recipe(self):
        recipe_title = 'Recipe Title'

        self.create_recipe_and_login()

        response = self.client.get(reverse('authors:recipe_edit', kwargs={'id': 1}), follow=True)
        content = response.content.decode('utf-8')

        self.assertIn(recipe_title, content)

    def test_succesfully_recipe_edit(self):
        self.create_recipe_and_login()

        url = reverse('authors:recipe_edit', kwargs={'id': 1})
        response = self.client.post(url, data=self.recipe_form_data, follow=True)

        msg = 'Sua receita foi editada com sucesso!'

        self.assertIn(msg, response.content.decode('utf-8'))
    
    def test_edited_recipe_is_not_published(self):
        self.create_recipe_and_login()
        self.recipe_form_data['title'] = 'Change title.'
        
        url = reverse('authors:recipe_edit', kwargs={'id': 1})
        self.client.post(url, data=self.recipe_form_data, follow=True)
        recipe = get_object_or_404(Recipe, id=1)

        self.assertFalse(recipe.is_published)
