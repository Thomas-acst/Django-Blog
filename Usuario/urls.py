from django.contrib import admin
from django.urls import path, include
from . import views
from .models import Info_User

urlpatterns = [
    path('valida_login/', views.valida_login, name ='valida_login'),
    path('valida_cadastro/', views.valida_cadastro, name ='valida_cadastro'),

    path('cadastrar/', views.cad, name ='cadastro'),
    path('logar/', views.logar, name ='login'),  
    path('sair/', views.deslogar, name='deslogar'),
    path('perfil/<str:username>/', views.perfil, name='perfil')
]
