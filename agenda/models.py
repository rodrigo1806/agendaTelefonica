from django.db import models

class Agenda(models.Model):
	nome = models.CharField(max_length=120)
	sobrenome = models.CharField(max_length=120)
	cidade = models.CharField(max_length=120)
	telefone = models.CharField(max_length=30)
	email = models.CharField(max_length=130)

