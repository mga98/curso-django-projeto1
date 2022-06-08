from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase, Recipe


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_raises_error_if_has_more_than_65_chars(self):
        self.recipe.title = 'A' * 70  # Multiplies the title for 70.

        with self.assertRaises(ValidationError):
            """
            Checks if the code below raises a ValidationError
            """
            self.recipe.full_clean()  # Full clean to force the validation of the title max lenght.
        
    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
        )

        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):      
        setattr(self.recipe, field, 'A' * (max_length + 1))  # Set an attribute to each field in self.recipe.

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()

        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe preparation_steps_is_html is not False.'
            )
    
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()

        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published is not False'
        )

    def test_recipe_string_representation(self):
        needed_title = 'Testing Representation Title'
        self.recipe.title = needed_title
        self.recipe.full_clean()
        self.recipe.save()
        str(self.recipe)

        self.assertEqual(str(self.recipe), needed_title)
        