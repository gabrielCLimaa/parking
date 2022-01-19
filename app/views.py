from django.shortcuts import render , redirect 
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .forms import *
from .models import *
from django.utils import timezone
import datetime

# Create your views here.
VEICULO_JA_ESTACIONADO = -1
VEICULO_PRONTO = 1
NOT_EXIST = NULL

@login_required
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

@login_required
@permission_required('app.vaga_perm')
def VagaCriar(request):

    if isToCreateOrUpdateObject(request):
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit = False)
            if carExistsInSpot(vaga):
                if checarVagas(vaga.carro.placa) == VEICULO_JA_ESTACIONADO:
                    return render(request, 'error/erro_vaga_criar.html')
                TriggerCreateTicket(vaga.carro.placa)
        vaga.save()
        return redirect('vagas')
    else:
        form = VagaForm
        return render(request, 'vaga_criar.html',{'form': form})

@login_required
@permission_required('app.vaga_perm')
def VagaAtualizar(request,pk):
    if isToCreateOrUpdateObject(request):
        placaParaTicketDeSaida = getPreviewsCarIfExist(pk)

        form = VagaForm(request.POST,instance=Vaga.objects.get(pk=pk))

        if form.is_valid():
            vaga = form.save(commit = False)

            if placaParaTicketDeSaida != NOT_EXIST:
                generateExitTicket(vaga, placaParaTicketDeSaida)
            
            if carExistsInSpot(vaga):
                if checarVagas(vaga.carro.placa) == VEICULO_JA_ESTACIONADO:
                    return render(request, 'error/erro_vaga_criar.html') 
                TriggerCreateTicket(vaga.carro.placa)

            vaga.save()
            return redirect('tickets')
    else:
        form = VagaForm()
        return render(request, 'vaga_atualizar.html',{'form': form})

@login_required
@permission_required('app.vaga_perm')
def VagaDeletar(request,pk):
    vaga = Vaga.objects.get(pk=pk)

    if contemVeiculo(vaga):
        return render(request, 'error/erro_vaga_deletar.html')
    
    vaga.delete()

    return redirect('vagas')

class VagaListView(generic.ListView):
    model = Vaga

class VagaDetailView(generic.DetailView):
    model = Vaga

class CarroListView(generic.ListView):
    model = Carro

class CarroCreate(PermissionRequiredMixin,generic.CreateView):
    permission_required = 'app.carro_perm'
    model = Carro
    fields = '__all__'

class CarroUpdate(PermissionRequiredMixin,generic.UpdateView):
    permission_required = 'app.carro_perm'
    model = Carro
    fields = '__all__'

class CarroDelete(PermissionRequiredMixin,generic.DeleteView):
    permission_required = 'app.carro_perm'
    model = Carro
    success_url = reverse_lazy('carros')

class TicketListView(generic.ListView):
    model = Ticket

def getPreviewsCarIfExist(pk):
    vaga = Vaga.objects.get(pk=pk)
    plate = NOT_EXIST

    if carExistsInSpot(vaga):
        plate = vaga.carro.placa
    return plate

def isToCreateOrUpdateObject(request):
    if request.method == 'POST':
        return True
    return False

def carExistsInSpot(vaga):
    if vaga.carro != None:
        return True
    return False

def generateExitTicket(vaga,placa):
    if not(carExistsInSpot(vaga)):
        cacularTicket(timezone.now(), placa)

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

    if horarioDaEstadia > datetime.timedelta(hours=1) and horarioDaEstadia <  datetime.timedelta(hours=3):
        return 25

    if horarioDaEstadia > datetime.timedelta(hours=3) and horarioDaEstadia < datetime.timedelta(hours=6):
        return 45

    if horarioDaEstadia > datetime.timedelta(hours=6):
        return 55

def contemVeiculo(vaga):
    if vaga.carro == None:
        return False
    else: 
        return True

