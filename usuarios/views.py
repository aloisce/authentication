from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages, auth
from . models import Users


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/plataforma/home/')
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})

def login(request):
    if request.user.is_authenticated:
        return redirect('/plataforma/home/')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    cep = request.POST.get('cep')
    rua = request.POST.get('rua')
    numero = request.POST.get('numero')

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Nome e email nao podem estar vazios.')
        return redirect('/auth/cadastro/')
    
    if len(senha) < 8:
        messages. add_message(request, constants.ERROR, 'Sua senha deve ter no mínimo 8 caracteres.')
        return redirect('/auth/cadastro/')

    if Users.objects.filter(email = email).exists():
        messages.add_message(request, constants.ERROR, 'Já existe usuário com esse email.')
        return redirect('/auth/cadastro/')

    if Users.objects.filter(username = nome).exists():
        messages.add_message(request, constants.ERROR, 'Já existe um usuario com esse nome.')
        return redirect('/auth/cadastro/')
    
    try:
        usuario = Users.objects.create_user(username = nome,
                                            email = email,
                                            password = senha,
                                            rua = rua,
                                            numero = numero,
                                            cep = cep)
        usuario.save()
        
        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso!')
        return redirect('/auth/cadastro/')
    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema.')
        return redirect('/auth/cadastro/')

def valida_login(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')

    usuario = auth.authenticate(request, username = nome, password = senha)

    if not usuario:
        messages.add_message(request, constants.WARNING, 'Email ou senha inválido.')
        return redirect('/auth/login/')
    else:
        auth.login(request, usuario)
        return redirect('/plataforma/home/')

def sair(request):
    auth.logout(request)
    messages.add_message(request, constants.WARNING, 'Você saiu do sistema.')
    return redirect('/auth/login/')
