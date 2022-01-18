from asyncio.windows_events import NULL
from django.urls import reverse
from django.db import models
import uuid

# Create your models here.

class Estacionamento(models.Model):
    nome = models.CharField(max_length=10)

class Carro(models.Model):
    placa = models.CharField(primary_key=True, max_length=8)
    marca = models.CharField(max_length=10)
    modelo = models.CharField(max_length=10)

    def get_absolute_url(self):
        return reverse('carros')

class Vaga(models.Model):
    estacionamento = models.ForeignKey(Estacionamento,on_delete=models.RESTRICT, null=False)
    carro  = models.ForeignKey(Carro, on_delete=models.RESTRICT, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('vaga_details', args=[str(self.id)])

class Ticket(models.Model):
    horaDeEntrada = models.DateTimeField(auto_now_add=True)
    horaDeSaida = models.DateTimeField(null=True, blank=True)
    placaVeiculo = models.CharField(max_length=8)
    valor = models.FloatField(null=True, blank=True)

