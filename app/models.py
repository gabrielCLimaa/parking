from asyncio.windows_events import NULL
from django.db import models
import uuid

# Create your models here.


class Estacionamento(models.Model):
    nome = models.CharField(max_length=10)

class Carro(models.Model):
    placa = models.CharField(primary_key=True, max_length=8)
    marca = models.CharField(max_length=10)
    modelo = models.CharField(max_length=10)

class Vaga(models.Model):
    estacionamento = models.ForeignKey(Estacionamento,on_delete=models.RESTRICT, null=False)
    carro  = models.ForeignKey(Carro, on_delete=models.RESTRICT, null=True, blank=True)
    ocupado = models.BooleanField(default=False)

class Ticket(models.Model):
    horaDeEntrada = models.DateTimeField(null=False)
    horaDeSaida = models.DateTimeField(null=True, blank=True)
    placaVeiculo = models.CharField(max_length=8)
    valor = models.FloatField(null=True, blank=True)

