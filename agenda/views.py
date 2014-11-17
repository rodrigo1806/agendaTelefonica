from django.shortcuts import render, HttpResponseRedirect
from agenda.forms import AgendaForm, LoginForm, CadastroForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login as faz_login
from agenda.models import Agenda, Login

def index(request):
	loginForm = LoginForm()
	return render(request, 'index.html', {'loginForm': loginForm})

def entrar(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			usuario = authenticate(username=form.data['login'], password=form.data['senha'])
			request.session['loginUsuario'] = form.data['login']
			if usuario is not None:
				if usuario.is_active:
					faz_login(request, usuario)
					return HttpResponseRedirect('/lista/')
				else:
					return HttpResponseRedirect('/')
			else:
				return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')

@login_required()
def agenda(request):
	agendaForm = AgendaForm()
	return render(request, 'agenda.html', {'agendaForm': agendaForm})

def salvar(request):
	if request.method == 'POST':
		codigo = request.POST.get('codigo', '0')

		try:
			agenda = Agenda.objects.get(pk=codigo)
		except:
			agenda = Agenda()

		form = AgendaForm(request.POST)
		agenda.nome = form.data['nome']
		agenda.sobrenome = form.data['sobrenome']
		agenda.cidade = form.data['cidade']
		agenda.telefone = form.data['telefone']
		agenda.email = form.data['email']
		#request.session.get e uma variavel global
		agenda.loginUsuario = request.session.get('loginUsuario')
		agenda.save()
		contatos = Agenda.objects.all()[0:10]
		return render(request, 'lista.html', {'contatos': contatos})

@login_required()
def lista(request):
	contatos = Agenda.objects.filter(loginUsuario=request.session.get('loginUsuario'))
	return render(request, 'lista.html', {'contatos': contatos})

def editar(request, pk=0):
	try:
		agenda = Agenda.objects.get(pk=pk)
	except:
		return HttpResponseRedirect('/lista/')
    
	agendaForm = AgendaForm(initial={'nome': agenda.nome, 'sobrenome': agenda.sobrenome, 'cidade': agenda.cidade, 'telefone': agenda.telefone, 'email': agenda.email})
	return render(request, 'agenda.html', {'agendaForm': agendaForm, 'agendapk': agenda.pk})

def excluir(excluir, pk=0):
	try:
		agenda = Agenda.objects.get(pk=pk)
		agenda.delete()
		return HttpResponseRedirect('/lista/')
	except:
		return HttpResponseRedirect('/lista/')

def cadastro(request):
	cadastroForm = CadastroForm()
	return render(request, 'cadastro.html', {'cadastroForm': cadastroForm})

def salvaCadastro(request):
    if request.method == 'POST':
        loginForm = CadastroForm(request.POST)

        if loginForm.is_valid():
            login = Login(
                username=loginForm.data['login'],
                is_active=True)

            login.set_password(loginForm.data['senha'])
            login.save()

            loginForm = LoginForm()
            return render(request, 'index.html', {'loginForm': loginForm})
        else:
			cadastroForm = CadastroForm()
			return render(request, 'cadastro.html', {'cadastroForm': cadastroForm})

def sair(request):
	logout(request)
	return HttpResponseRedirect('/')


