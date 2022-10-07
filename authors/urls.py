from django.urls import path

from . import views

urlpatterns = [
    path(route='register/', view=views.register_author, name='register_view'),
]
