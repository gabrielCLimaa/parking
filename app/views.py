from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import *
from .models import *
from django.utils import timezone
import datetime

# Create your views here.

def index(request):
    vagas = Vaga.objects.count()
    carros = Carro.objects.count()
    tickets = Ticket.objects.count()

    context = {
        'vagas' : vagas,
        'carros' : carros,
        'tickets' : tickets
    }

    return render(request, 'index.html', context=context)

class VagaListView(generic.ListView):
    model = Vaga

class VagaDetailView(generic.DetailView):
    model = Vaga

def cacularTicket(horaSaida, placa):
    ticket = Ticket.objects.get(placaVeiculo=placa,valor=0)
    horario = horaSaida- ticket.horaDeEntrada

    if horario < datetime.timedelta(hours=1):
        ticket.valor = 15

    if horario > datetime.timedelta(hours=1):
        ticket.valor = 25

    if horario > datetime.timedelta(hours=3):
        ticket.valor = 45

    if horario > datetime.timedelta(hours=6):
        ticket.valor = 55

    ticket.horaDeSaida = horaSaida
    ticket.save()

def TriggerCreateTicket(placa):
    ticket = Ticket(
        placaVeiculo = str(placa),
        valor = 0
    )
    ticket.save()


def VagaCriar(request):
    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)

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
                TriggerCreateTicket(str(vagaForm.carro.placa))

            vagaForm.save()
            return redirect('tickets')

    form = VagaForm()
    return render(request, 'vaga_atualizar.html',{'form': form})

class VagaDelete(generic.DeleteView):
    model = Vaga
    success_url = reverse_lazy('vagas')

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