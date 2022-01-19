from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vagas/', views.VagaListView.as_view(), name='vagas'),
    path('vaga/<int:pk>', views.VagaDetailView.as_view(), name='vaga_details'),
    path('vaga/create/', views.VagaCriar, name='vaga_create'),
    path('vaga/<int:pk>/update/', views.VagaAtualizar, name='vaga_update'),
    path('vaga/<int:pk>/delete/', views.VagaDeletar, name='vaga_delete'),
    path('carros/', views.CarroListView.as_view(), name='carros'),
    path('carro/create/', views.CarroCreate.as_view(), name='carro_create'),
    path('carro/<str:pk>/update/', views.CarroUpdate.as_view(), name='carro_update'),
    path('carro/<str:pk>/delete/', views.CarroDelete.as_view(), name='carro_delete'),
    path('tickets/', views.TicketListView.as_view(), name='tickets')
]
