from django.contrib.auth.models import User
from django.urls import resolve, reverse
from parameterized import parameterized

from recipes.tests.test_recipe_base import RecipeMixin, RecipeTestBase


class RecipeEditTestUnitTest(RecipeTestBase, RecipeMixin):
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

    def test_recipe_edit_loads_correct_recipe(self):
        recipe_title = 'Recipe Title'

        self.make_recipe()
        self.client.login(
            username='username',
            password='123456',
        )

        response = self.client.get(reverse('authors:recipe_edit', kwargs={'id': 1}), follow=True)
        content = response.content.decode('utf-8')

        self.assertIn(recipe_title, content)

    def test_succesfully_recipe_edit(self):
        self.make_recipe()
        self.client.login(
            username='username',
            password='123456'
        )

        url = reverse('authors:recipe_edit', kwargs={'id': 1})
        response = self.client.post(url, data=self.recipe_create_data, follow=True)

        msg = 'Sua receita foi editada com sucesso!'

        self.assertIn(msg, response.content.decode('utf-8'))
