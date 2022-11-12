from django.urls import reverse

from .test_authors_base import AuthorsTestBase


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
