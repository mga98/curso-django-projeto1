from django.contrib import admin
from .models import Category, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'is_published', 'preparation_steps_is_html')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'id', 'description', 'slug', 'author__username')
    list_filter = ('category', 'author', 'is_published', 'preparation_steps_is_html')
    list_per_page = 10
    list_editable = ('is_published', 'preparation_steps_is_html')
    ordering = ('-id', '-created_at')
    prepopulated_fields = {
        'slug': ('title',)
    }
