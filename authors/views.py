from django.shortcuts import render


def register_view(request):
    return render(request, 'author/pages/register_view.html')
