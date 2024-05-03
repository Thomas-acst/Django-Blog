from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('home/<str:username>/', views.home, name='home'),
    path('form_post/', views.form_post, name='form_post'),
    path('botao_post/', views.botao_post, name='botao_post'),
    path('noticia_completa/<int:id>/', views.noticia_completa, name ='noticia_completa'),
    path('editar_post/<int:id>', views.editar, name ='editar_post'),
    path('excluir_post/<int:id>', views.excluir, name ='excluir_post'),
    path('edit_post/<str:username>', views.edit_perfil, name='editar_perfil')

]
