from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import FormRegister

# Create your views here.


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = FormRegister(register_form_data)
    return render(request=request,
                  template_name='authors/pages/register_view.html',
                  context={
                      'form': form,
                      'form_action': reverse(viewname='authors:create')
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
