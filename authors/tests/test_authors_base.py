from django.test import TestCase
from django.contrib.auth.models import User

from recipes.tests.test_recipe_base import RecipeMixin


class AuthorsTestBase(TestCase, RecipeMixin): 
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

    def create_recipe_and_login(self):
        self.make_recipe()
        self.client.login(
            username='username',
            password='123456',
        )