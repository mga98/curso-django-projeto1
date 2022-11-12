from django.urls import reverse

from .test_authors_base import AuthorsTestBase


class AuthorDashboard(AuthorsTestBase):
    def test_dashboard_loads_recipes(self):
        self.make_recipe(
            title='Recipe in dashboard'
        )

        self.client.login(
            username='username',
            password='123456'
        )

        url = reverse('authors:dashboard')
        response = self.client.get(url, follow=True)
        recipe = 'Recipe in dashboard'

        self.assertIn(recipe, response.content.decode('utf-8'))

    def test_empty_dashboard(self):
        self.user_register_and_login()

        url = reverse('authors:dashboard')
        response = self.client.get(url, follow=True)
        msg = 'Você ainda não tem nenhuma receita publicada.'

        self.assertIn(msg, response.content.decode('utf-8'))
