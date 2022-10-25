from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .test_base import RecipeBaseFunctionalTest
from unittest.mock import patch
import pytest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here.', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        title_needed = 'Title needed'

        recipes[0].title = title_needed
        recipes[0].save()

        self.browser.get(self.live_server_url)

        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Pesquise sua receita aqui..."]'
        )
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        body = self.browser.find_element(By.CLASS_NAME, 'main-content-list').text

        self.assertIn(
            title_needed,
            body
        )
