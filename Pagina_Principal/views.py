from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from Usuario import views
from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Postagem
from Usuario.models import Info_User


def home(request, username):
    usuario = Info_User.objects.get(username=username)
    todas_postagens = Postagem.objects.all()
    context = {'usuario': usuario, 'todas_postagens': todas_postagens}
    if request.user.is_authenticated:
        return render(request, 'home.html', context)
    else:
        return render(request, 'login.html')


def botao_post(request):
    return render(request, 'post.html')


def form_post(request):

    titulo = request.POST.get('titulo')
    conteudo = request.POST.get('conteudo')

    autor = request.user
    postagem = Postagem(titulo=titulo, conteudo=conteudo, autor=autor)
    postagem.save()
    return redirect('home', username=request.user.username)


def noticia_completa(request, id):
    usuario_atual = request.user
    noticia = Postagem.objects.get(id=id)
    context = {'noticia': noticia, 'usuario_atual': usuario_atual}
    return render(request, 'noticia.html', context)


def editar(request, id):
    post = get_object_or_404(Postagem, id=id)
    usuario = Info_User.objects.get(id=post.autor_id)
    if request.method == "POST":
        post.titulo = request.POST.get("novo_titulo")
        post.conteudo = request.POST.get("novo_conteudo")
        post.save()
        postagens = Postagem.objects.filter(autor=usuario)
        return render(request, 'perfil.html', {"usuario": usuario, "postagens": postagens})
    else:
        return render(request, 'edit.html', {"post": post, "usuario": usuario})


def excluir(request, id):
    postagem = get_object_or_404(Postagem, id=id)
    usuario = Info_User.objects.get(id=postagem.autor_id)
    postagem.delete()
    postagens = Postagem.objects.filter(autor=usuario)
    return render(request, "perfil.html", {"usuario": usuario, "postagens": postagens})


def edit_perfil(request, username):
    usuario = Info_User.objects.get(username=username)
    if request.method == "POST":
        usuario.username = request.POST.get("nome")
        usuario.email = request.POST.get("email")
        usuario.nickname = request.POST.get("apelido")
        usuario.nascimento = request.POST.get("nascimento")
        usuario.save()
        # linha abaixo destinada a atualização das notícias
        postagens = Postagem.objects.filter(autor=usuario)
        return render(request, "perfil.html", {'usuario': usuario, "postagens": postagens})
    else:
        return render(request, 'edit_perfil.html', {"usuario": usuario})
