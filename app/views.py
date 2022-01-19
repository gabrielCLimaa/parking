from django.shortcuts import render , redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from .forms import *
from .models import *
from django.utils import timezone
import datetime

# Create your views here.
VEICULO_JA_ESTACIONADO = -1
VEICULO_PRONTO = 1

def index(request):
    vagas = Vaga.objects.count()
    carros = Carro.objects.count()
    tickets = Ticket.objects.count()
    vagas_disponiveis = Vaga.objects.filter(carro=None).count()

    context = {
        'vagas' : vagas,
        'carros' : carros,
        'tickets' : tickets,
        'vagas_disponiveis' : vagas_disponiveis
    }

    return render(request, 'index.html', context=context)

class VagaListView(generic.ListView):
    model = Vaga

class VagaDetailView(generic.DetailView):
    model = Vaga

def VagaCriar(request):
    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)

            if vaga.carro != None:
                if vaga.carro.placa:
                    TriggerCreateTicket(str(vaga.carro.placa))

            vaga.save()
            return redirect('vagas')

    form = VagaForm
    return render(request, 'vaga_criar.html',{'form': form})

def VagaAtualizar(request,pk):
    if request.method == 'POST':
        vaga = Vaga.objects.get(pk=pk)
 
        placaParaTicketDeSaida = NULL

        if vaga.carro != None:
            placaParaTicketDeSaida = vaga.carro.placa

        form = VagaForm(request.POST, instance=vaga)
        if form.is_valid():
            vagaForm = form.save(commit = False)

            if placaParaTicketDeSaida != NULL:
                if vagaForm.carro == None:
                    cacularTicket(timezone.now(), placaParaTicketDeSaida)

            if vagaForm.carro != None:
                if checarVagas(vagaForm.carro.placa) == VEICULO_JA_ESTACIONADO:
                    return render(request, 'error/erro_vaga_criar.html')
                TriggerCreateTicket(str(vagaForm.carro.placa))

            vagaForm.save()
            return redirect('tickets')

    form = VagaForm()
    return render(request, 'vaga_atualizar.html',{'form': form})

def checarVagas(placa):
    carro = Carro.objects.get(placa=placa)
    vagas = Vaga.objects.filter(carro=carro)

    if vagas.exists():
        return VEICULO_JA_ESTACIONADO
    else:
        return VEICULO_PRONTO

def TriggerCreateTicket(placa):
    ticket = Ticket(
        placaVeiculo = str(placa),
        valor = 0
    )
    ticket.save()

def cacularTicket(horaSaida, placa):
    ticket = Ticket.objects.get(placaVeiculo=placa,valor=0)
    horario = horaSaida - ticket.horaDeEntrada
    ticket.valor = calcularValor(horario)
    ticket.horaDeSaida = horaSaida
    ticket.save()

def calcularValor(horarioDaEstadia):
    if horarioDaEstadia < datetime.timedelta(hours=1):
        return 15

    if horarioDaEstadia > datetime.timedelta(hours=1):
        return 25

    if horarioDaEstadia > datetime.timedelta(hours=3):
        return 45

    if horarioDaEstadia > datetime.timedelta(hours=6):
        return 55

def contemVeiculo(vaga):
    if vaga.carro == None:
        return False
    else: 
        return True

def VagaDeletar(request,pk):
    vaga = Vaga.objects.get(pk=pk)

    if contemVeiculo(vaga):
        return render(request, 'error/erro_vaga_deletar.html')
    
    vaga.delete()

    return redirect('vagas')
    
class CarroListView(generic.ListView):
    model = Carro
    
class CarroCreate(generic.CreateView):
    model = Carro
    fields = '__all__'

class CarroUpdate(generic.UpdateView):
    model = Carro
    fields = '__all__'

class CarroDelete(generic.DeleteView):
    model = Carro
    success_url = reverse_lazy('carros')

class TicketListView(generic.ListView):
    model = Ticket