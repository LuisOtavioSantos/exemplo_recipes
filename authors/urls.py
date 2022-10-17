from django.urls import path

from . import views

app_name = 'authors'

urlpatterns = [
    path(route='register/', view=views.register_view, name='register'),
    path(route='register/create/',
         view=views.register_create, name='register_create'),
    path(route='login/', view=views.login_view, name='login'),
    path(route='login/create', view=views.login_create, name='login_create'),
    path(route='logout/', view=views.logout_view, name='logout'),
    path(route='dashboard/', view=views.dashboard, name='dashboard'),
]
