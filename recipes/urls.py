from django.urls import path

from .views import contato, home, sobre

urlpatterns = [
    path('', home, name='index'),
    path('contato/', contato, name='index'),
    path('sobre/', sobre, name='sobre')
]
