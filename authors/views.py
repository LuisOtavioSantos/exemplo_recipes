from django.http import Http404
from django.shortcuts import redirect, render

from .forms import FormRegister

# Create your views here.


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = FormRegister(register_form_data)
    return render(request=request,
                  template_name='authors/pages/register_view.html',
                  context={'form': form})


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = FormRegister(POST)

    return redirect(to='authors:register')
