from django.shortcuts import render

# Create your views here.


def register_author(request):
    return render(request=request, template_name='authors/pages/register_view.html')
