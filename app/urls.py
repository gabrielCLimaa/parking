from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vagas/', views.VagaListView.as_view(), name='vagas'),
    path('vaga/<int:pk>', views.VagaDetailView.as_view(), name='vaga_details'),
    path('vaga/create/', views.VagaCreate.as_view(), name='vaga_create'),
    path('vaga/<int:pk>/update/', views.VagaUpdate.as_view(), name='vaga_update'),
    path('vaga/<int:pk>/delete/', views.VagaDelete.as_view(), name='vaga_delete')
]
