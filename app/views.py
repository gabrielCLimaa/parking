from django.shortcuts import render
from django.views import generic
from .models import *

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

