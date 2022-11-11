from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.text import slugify
from django.urls import reverse
from recipes.models import Recipe

from .forms import LoginForm, RegisterForm, AuthorsRecipeForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)

    return render(request, 'author/pages/register_view.html', context={
        'form': form,
        'form_action': reverse('authors:register_create')
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(
            request, 'Você foi registrado com sucesso! Faça seu login.')

        del(request.session['register_form_data'])

        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()

    return render(request, 'author/pages/login_view.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Você foi logado com sucesso!')
            login(request, authenticated_user)

            return redirect(reverse('authors:dashboard'))

        else:
            messages.error(request, 'Login ou senha inválidos.')

    else:
        messages.error(
            request, 'Erro ao validar as informações do formulário.')

    return redirect(login_url)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Logout não pode ser executado!')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Usuário de logout inválido!')
        return redirect(reverse('authors:login'))

    logout(request)
    messages.warning(request, 'Você foi deslogado.')
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_view(request):
    recipes = Recipe.objects.filter(
        author=request.user,
    ).order_by('-id')

    return render(request, 'author/pages/dashboard_view.html', context={
        'recipes': recipes,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def recipe_edit(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    form = AuthorsRecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Sua receita foi editada com sucesso!')

        return redirect(reverse('authors:dashboard'))

    return render(request, 'author/pages/dashboard_edit_view.html', context={
        'recipe': recipe,
        'form': form,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def recipe_create(request):
    form = AuthorsRecipeForm(
        request.POST or None,
        files=request.FILES or None,
    )

    try:
        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.slug = slugify(recipe.title, allow_unicode=True)

            recipe.save()

            messages.success(request, 'Sua receita foi criada com sucesso!')

            return redirect(reverse('authors:dashboard'))

    except TypeError:
        messages.error(request, 'Erro ao validar formulário!')

        return redirect(reverse('authors:recipe_create'))
    
    return render(request, 'author/pages/dashboard_edit_view.html', context={
        'form': form,
    })

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404
 
    POST = request.POST
    id = POST.get('id')

    recipe = get_object_or_404(Recipe, id=id)

    recipe.delete()
    messages.info(request, f'Receita ({recipe.title}) deletada com sucesso!')

    return redirect(reverse('authors:dashboard'))
