from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/recipe/<int:id>/edit', views.RecipeEdit.as_view(), name='recipe_edit'),
    path('dashboard/recipe/create', views.RecipeCreate.as_view(), name='recipe_create'),
    path('dashboard/recipe/delete', views.dashboard_recipe_delete, name='recipe_delete'),
]
