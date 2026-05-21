from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('disponibilidad/', views.consulta_disponibilidad, name='disponibilidad'),
    path('agenda/', views.agenda_diaria, name='agenda'),
    path('reporte/', views.reporte_reservas, name='reporte'),
]
