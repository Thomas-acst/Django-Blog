import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Usuario.models import Info_User
from Pagina_Principal.models import Postagem
from django.contrib.auth import *
from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import *
import hashlib
from django.contrib.auth.models import AnonymousUser


def cad(request):
    return render(request, "cadastro.html")


def logar(request):
    return render(request, "login.html")


def valida_cadastro(request):

    # Salvando usuário no banco de dado

    usuario = Info_User()

    usuario.username = request.POST.get('username')
    usuario.nickname = request.POST.get('nickname')
    usuario.nascimento = request.POST.get('data')
    usuario.email = request.POST.get('email')
    usuario.set_password(request.POST.get('senha'))

    padrao_email = r'([\w\.\-@])*(@gmail.com|\@hotmail.com|\@yahoo.com|\@icloud.com|\@edu.br|gov.br)'
    ano_hoje = date.today().year
    data_nascimento = datetime.strptime(usuario.nascimento, "%Y-%m-%d")

    # validando nome
    if len(usuario.username) == 0:
        messages.error(request, "Você não preencheu seu nome!")
        return redirect('cadastro')

    # validando nickname
    if len(usuario.nickname) == 0:
        messages.error(request, "Você não preencheu seu nickname!")
        return redirect('cadastro')

    # validando data
    if not usuario.nascimento:
        messages.error(request, "Data de nascimento vazia e ou inválida!")
        return redirect('cadastro')
    if ano_hoje - (data_nascimento).year <= 18:
        messages.error(request, "Você é menor de idade!")
        return redirect('cadastro')

    if len(usuario.email) == 0:
        messages.error(request, "Você não preencheu seu email!")
        return redirect('cadastro')
    if not re.match(padrao_email, usuario.email):
        messages.error(request, "Tem algum erro no seu email!")
        return redirect('cadastro')

    # validando senha
    # if len(senha) == 0:
    #     messages.error(request, "Você não preencheu sua senha!")
    #     return redirect('cadastro')

    # if len(senha) == 0 or len(usuario.email.strip()) == 0 or len(usuario.username.strip()) == 0 or len(usuario.nickname.strip()) == 0:
    #     messages.error(
    #         request, "Você tentou colocar espaço para indicar caractere né?")
    #     return redirect('cadastro')

    if Info_User.objects.filter(username=usuario.username):
        messages.error(request, 'Nome já cadastrado!')
        return redirect('cadastro')
    if Info_User.objects.filter(email=usuario.email):
        messages.error(request, 'Email já cadastrado!')
        return redirect('cadastro')
    elif Info_User.objects.filter(nickname=usuario.nickname):
        messages.error(request, 'Apelido já cadastrado!')
        return redirect('cadastro')
    # Para verificação usei este site: https://www.w3schools.com/django/django_queryset_filter.php
    # senha_codificada = senha
    # usuario.password = senha_codificada
    # '''    senha_codificada = hashlib.sha256(senha.encode()).hexdigest()
    #        usuario.password = senha_codificada  '''
    usuario.save()
    return render(request, "login.html")  # menssagem aqui

    # return HttpResponse(f"{nome} / {sobrenome} / {apelido} / {data_nascimento} / {email} / {senha}")


def valida_login(request):
    usuario = Info_User()
    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.senha = request.POST.get('senha')

        user = authenticate(username=usuario.username,
                            email=usuario.email, password=usuario.senha)
        login(request, user)
        print("Usuário autenticado:", user)
        return redirect('perfil', username=usuario.username)


'''    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # validando nome
        if len(username) == 0:
            messages.error(request, "Você não preencheu seu nome!")
            return redirect('login')
        # validando email
        if len(email) == 0:
            messages.error(request, "Você não preencheu seu email!")
            return redirect('login')
        # validando senha
        if len(senha) == 0:
            messages.error(request, "Você não preencheu sua senha!")
            return redirect('login')

        print("Dados recebidos:", username, email, senha)

        user = authenticate(request, username=username,
                            email=email, password=senha)
        if isinstance(user, AnonymousUser):
            # Se o usuário for anônimo, significa que a autenticação falhou
            messages.error(request, "Email e/ou senha inválidos!")
            return redirect('login')

        # if user is not None:
        login(request, user)
        print("Usuário autenticado:", user)
        return redirect('perfil', username=username)
        # else:
        #    messages.error(request, "Email e/ou senha inválidos!")
        #    return redirect('login')
    else:
        return redirect('login')'''


@ login_required
def deslogar(request):
    logout(request)
    return render(request, 'cadastro.html')


def perfil(request, username):
    usuario = Info_User.objects.get(username=username)
    postagens = Postagem.objects.filter(autor=usuario)
    context = {'usuario': usuario, 'postagens': postagens}
    if request.user.is_authenticated:
        return render(request, 'perfil.html', context)
    else:
        return HttpResponse('<h1> Faça Login para acessar seu perfil! </h1>')
