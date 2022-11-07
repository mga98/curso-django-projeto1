from django import forms

from recipes.models import Recipe
from utils.django_forms import add_attr


class AuthorsRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'preparation_time', 'preparation_time_unit',
                  'preparation_steps', 'servings', 'servings_unit', 'cover', 'category')

        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2',
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Unidade', 'Unidades'),
                    ('Copos', 'Copos'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices={
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'span-2',
                }
            ),
        }

        prepopulated_fields = {
        'slug': ('title',)
        }
