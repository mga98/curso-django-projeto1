from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    context = {}
    context['name'] = 'Miguel'
    return render(request, 'recipes/home.html', context)

 
def contato(request):
    return render(request)


def sobre(request):
    return render(request)
