from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('disponibilidad/', views.consulta_disponibilidad, name='disponibilidad'),
    path('agenda/', views.agenda_diaria, name='agenda'),
    path('reporte/', views.reporte_reservas, name='reporte'),
    path('crear/', views.crear_reserva, name='crear_reserva'),
    path('espacios/', views.mis_espacios, name='mis_espacios'),
    path('espacios/nuevo/', views.crear_espacio, name='crear_espacio'),
]
