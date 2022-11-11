from django.contrib.auth.models import User
from django.urls import reverse

from recipes.tests.test_recipe_base import RecipeMixin, RecipeTestBase


class RecipeFormUnitTest(RecipeTestBase, RecipeMixin):
    def setUp(self, *args, **kwargs):
        self.recipe_form_data = {
            'title': 'Recipe Title',
            'description': 'Recipe Description',
            'preparation_time': '1',
            'preparation_time_unit': 'Horas',
            'preparation_steps': 'A' * 11,
            'servings': '1',
            'servings_unit': 'Unidades',
        }

    def user_register_and_login(self):
        User.objects.create_user(
            username='usertest',
            password='Testuser@1'
        )

        self.client.login(
            username='usertest',
            password='Testuser@1',
        )

    def field_values_tests(self, field, value):
        self.user_register_and_login()

        self.recipe_form_data[field] = value

        url = reverse('authors:recipe_create')
        response = self.client.post(
            url,
            data=self.recipe_form_data,
            follow=True
        )

        return response

    def test_title_min_length_error(self):
        response = self.field_values_tests('title', 'min')

        msg = 'O título deve ter mais de 5 caracteres!'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_preparation_steps_min_length_error(self):
        response = self.field_values_tests('preparation_steps', 'min')

        msg = 'O preparo deve ter no mínimo 10 caracteres!'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_title_and_description_are_equal_error(self):
        self.user_register_and_login()

        field_name = 'Recipe'

        self.recipe_form_data['title'] = field_name
        self.recipe_form_data['description'] = field_name

        url = reverse('authors:recipe_create')
        response = self.client.post(url, data=self.recipe_form_data, follow=True)
        response_content = response.content.decode('utf-8')

        msg1 = 'O título deve ser diferente da descrição!'
        msg2 = 'A descrição deve ser diferente do título!'

        self.assertIn(msg1, response_content)
        self.assertIn(msg2, response_content)

    def test_preparation_negative_time_error(self):
        response = self.field_values_tests('preparation_time', '-1')

        msg = 'O tempo de preparo não pode ser negativo!'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_servings_negative_unit_error(self):
        response = self.field_values_tests('servings', '-1')

        msg = 'O número de porções não pode ser negativo!'

        self.assertIn(msg, response.content.decode('utf-8'))
