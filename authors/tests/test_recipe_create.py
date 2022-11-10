from django.contrib.auth.models import User
from django.urls import resolve, reverse
from parameterized import parameterized

from recipes.tests.test_recipe_base import RecipeMixin, RecipeTestBase


class RecipeCreateUnitTest(RecipeTestBase, RecipeMixin):
    def setUp(self, *args, **kwargs):
        self.recipe_create_data = {
            'title': 'Recipe Title',
            'description': 'Recipe Description',
            'preparation_time': '1',
            'preparation_time_unit': 'Horas',
            'preparation_steps': 'A' * 11,
            'servings': '1',
            'servings_unit': 'Unidades',
        }

        return super().setUp(*args, **kwargs)

    def user_register_and_login(self):
        User.objects.create_user(
            username='usertest',
            password='Testuser@1'
        )

        self.client.login(
            username='usertest',
            password='Testuser@1',
        )

    def test_recipe_succesfully_created(self):
        self.user_register_and_login()

        url = reverse('authors:recipe_create')
        response = self.client.post(
            url, data=self.recipe_create_data, follow=True)

        msg = 'Sua receita foi criada com sucesso!'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_recipe_create_form_not_valid(self):
        self.user_register_and_login()

        self.recipe_create_data['title'] = ''

        url = reverse('authors:recipe_create')
        response = self.client.post(url, data=self.recipe_create_data, follow=True)

        msg = 'Erro ao validar formulário!'

        self.assertIn(msg, response.content.decode('utf-8'))
