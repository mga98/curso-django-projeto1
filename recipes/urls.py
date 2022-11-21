from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeHome.as_view(), name='index'),
    path('recipe/search/', views.RecipeSearch.as_view(), name='search'),
    path('recipe/category/<int:category_id>/', views.RecipeCategory.as_view(), name='category'),
    path('recipe/<int:id>/', views.recipe, name='recipe'),
]
