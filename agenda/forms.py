from django import forms
from agenda.models import Agenda

class AgendaForm(forms.ModelForm):
	class Meta:
		model = Agenda

class LoginForm(forms.Form):
	login = forms.CharField(max_length='30', required=True)
	senha = forms.CharField(widget=forms.PasswordInput, required=True)

class CadastroForm(forms.Form):
	login = forms.CharField(max_length='30', required=True)
	senha = forms.CharField(widget=forms.PasswordInput, required=True)
	email = forms.CharField(max_length='130')