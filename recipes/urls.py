from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='index'),
    path('recipe/search/', views.search, name='search'),
    path('recipe/category/<int:category_id>/', views.category, name='category'),
    path('recipe/<int:id>/', views.recipe, name='recipe'),
]
