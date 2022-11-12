from django.urls import reverse

from .test_authors_base import AuthorsTestBase

class RecipeCreateUnitTest(AuthorsTestBase):
    def test_recipe_succesfully_created(self):
        self.user_register_and_login()

        url = reverse('authors:recipe_create')
        response = self.client.post(
            url, data=self.recipe_form_data, follow=True)

        msg = 'Sua receita foi criada com sucesso!'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_recipe_create_form_not_valid(self):
        self.user_register_and_login()

        self.recipe_form_data['title'] = ''

        url = reverse('authors:recipe_create')
        response = self.client.post(url, data=self.recipe_form_data, follow=True)

        msg = 'Erro ao validar formulário!'

        self.assertIn(msg, response.content.decode('utf-8'))
