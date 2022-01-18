from django.shortcuts import render
from django.urls import reverse_lazy
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

class VagaDetailView(generic.DetailView):
    model = Vaga

class VagaCreate(generic.CreateView):
    model = Vaga
    fields = '__all__'

class VagaUpdate(generic.UpdateView):
    model = Vaga
    fields = '__all__'

class VagaDelete(generic.DeleteView):
    model = Vaga
    success_url = reverse_lazy('vagas')