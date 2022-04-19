from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    context = {}
    context['name'] = 'Miguel'
    return render(request, 'recipes/pages/home.html', context)
