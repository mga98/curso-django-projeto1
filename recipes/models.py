from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Categoria', max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField('Título', max_length=65)
    description = models.CharField('Descrição', max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField('Tempo de preparo')
    preparation_time_unit = models.CharField('Tempo de preparo de unidade', max_length=65)
    servings = models.IntegerField('Porções')
    servings_unit = models.CharField('Unidade da porção', max_length=65)
    preparation_steps = models.TextField('Etapas de preparo')
    preparation_steps_is_html = models.BooleanField('HTML', default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    is_published = models.BooleanField('Publicado', default=False)
    cover = models.ImageField('Imagem', upload_to='recipes/cover/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(
        Category, verbose_name='Categoria', on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    author = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))
