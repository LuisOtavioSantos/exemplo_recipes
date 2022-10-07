from django.shortcuts import render

from .forms import FormRegister

# Create your views here.


def register_author(request):
    form = FormRegister()
    return render(request=request,
                  template_name='authors/pages/register_view.html',
                  context={'form': form})
