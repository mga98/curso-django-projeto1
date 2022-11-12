from django.urls import reverse

from .test_authors_base import AuthorsTestBase


class RecipeDeleteUnitTest(AuthorsTestBase):
    def test_recipe_delete_get_method_returns_404(self):
        self.create_recipe_and_login()

        url = reverse('authors:recipe_delete')
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 404)

    def test_recipe_deleted_succesfully(self):
        self.create_recipe_and_login()

        url = reverse('authors:recipe_delete')
        response = self.client.post(url, follow=True, data={'id': 1})

        msg = 'Receita (Recipe Title) deletada com sucesso!'

        self.assertIn(msg, response.content.decode('utf-8'))
