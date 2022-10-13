from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

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
        # form.save() # salva sem criptografar a senha
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(
            request=request, message='User created! \nLogin Available.')
        del (request.session['register_form_data'])
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

    login_url = reverse(viewname='authors:login')
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

    return redirect(to=login_url)
