from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from recipes.models import Recipe

from authors.forms.recipe_form import AuthorRecipeForm

from .forms import FormLogin, FormRegister

# Create your views here.


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = FormRegister(register_form_data)
    return render(request=request,
                  template_name='authors/pages/register_view.html',
                  context={
                      'form': form,
                      'form_action': reverse(viewname='authors:register_create')  # noqa E501
                  })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = FormRegister(POST)  # noqa F841
    if form.is_valid():
        # form.save() # save without encripting
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(
            request=request, message='User created! Login Available.')
        del (request.session['register_form_data'])
        return redirect(to='authors:login')
    else:
        return redirect(to='authors:register')


def login_view(request):
    form = FormLogin()
    return render(request=request,
                  template_name='authors/pages/login.html',
                  context={
                      'form': form,
                      'form_action': reverse(viewname='authors:login_create')
                  })


def login_create(request):
    if not request.POST:
        raise Http404()

    dashboard_url = reverse(viewname='authors:dashboard')
    form = FormLogin(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            request=request,
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if authenticated_user is not None:
            messages.success(
                request=request,
                message='You Are Logged In'
            )
            login(request=request, user=authenticated_user)
        else:
            messages.error(request=request, message='Invalid Credentials')
    else:
        messages.error(request=request, message='Invalid Password or Username')

    return redirect(to=dashboard_url)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request=request, message='Invalid logout request')
        return redirect(to='authors:login')

    if request.POST.get('username') != request.user.username:
        messages.error(request=request, message='Invalid logout user')
        return redirect(to='authors:login')

    messages.success(
        request=request, message='Logged out succeed! See you Later.')
    logout(request)
    return redirect(to='authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(
        request=request,
        template_name='authors/pages/dashboard.html',
        context={'recipes': recipes})


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id
    ).first()
    if not recipe:
        raise Http404()
    form = AuthorRecipeForm(
        data=request.POST or None,
        instance=recipe
    )
    return render(
        request=request,
        template_name='authors/pages/dashboard_recipe.html',
        context={
            'form': form
        })
