from django import forms
from django.core.exceptions import ValidationError
from collections import defaultdict

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive


class AuthorsRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list) 

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


    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        preparation_steps = cleaned_data.get('preparation_steps')

        if len(title) < 5:
            self._my_errors['title'].append('O título deve ter mais de 5 caracteres!')

        if len(preparation_steps) < 10:
            self._my_errors['preparation_steps'].append('O preparo deve ter no mínimo 10 caracteres!')

        if description == title:
            self._my_errors['title'].append('O título deve ser diferente da descrição!')
            self._my_errors['description'].append('A descrição deve ser diferente do título!')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean


    def clean_preparation_time(self):
        field_name = 'preparation_time'
        preparation_time = self.cleaned_data.get(field_name)
        
        if not is_positive(preparation_time):
            self._my_errors[field_name].append('O tempo de preparo não pode ser negativo!')

        return preparation_time

    def clean_servings(self):
        field_name = 'servings'
        servings = self.cleaned_data.get(field_name)

        if not is_positive(servings):
            self._my_errors[field_name].append('O número de porções não pode ser negativo!')

        return servings
