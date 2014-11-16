from django.shortcuts import render, HttpResponseRedirect
from agenda.forms import AgendaForm, LoginForm, CadastroForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login as faz_login
from agenda.models import Agenda

def index(request):
	loginForm = LoginForm()
	return render(request, 'index.html', {'loginForm': loginForm})

def entrar(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			usuario = authenticate(username=form.data['login'], password=form.data['senha'])

			if usuario is not None:
				if usuario.is_active:
					faz_login(request, usuario)
					return HttpResponseRedirect('/lista/')
				else:
					return render(request, 'index.html', {'form': form})
			else:
				return render(request, 'index.html', {'form': form})
		else:
			return render(request, 'index.html', {'form': form})
	else:
		return HttpResponseRedirect('/')

@login_required()
def agenda(request):
	agendaForm = AgendaForm()
	return render(request, 'agenda.html', {'agendaForm': agendaForm})

def salvar(request):
	if request.method == 'POST':
		form = AgendaForm(request.POST)
		agenda = Agenda()
		agenda.nome = form.data['nome']
		agenda.sobrenome = form.data['sobrenome']
		agenda.cidade = form.data['cidade']
		agenda.telefone = form.data['telefone']
		agenda.email = form.data['email']
		agenda.save()
		contatos = Agenda.objects.all()[0:10]
		return render(request, 'lista.html', {'contatos': contatos})

@login_required()
def lista(request):
	contatos = Agenda.objects.all()[0:10]
	return render(request, 'lista.html', {'contatos': contatos})

def editar(request, pk=0):
	try:
		agenda = Agenda.objects.get(pk=pk)
	except:
		return HttpResponseRedirect('/lista/')
    
	agendaForm = AgendaForm()
	agendaForm.nome = agenda.nome
	return render(request, 'agenda.html', {'agendaForm': agendaForm})

def excluir(excluir, pk=0):
	try:
		agenda = Agenda.objects.get(pk=pk)
		agenda.delete()
		return HttpResponseRedirect('/lista/')
	except:
		return HttpResponseRedirect('/lista/')


