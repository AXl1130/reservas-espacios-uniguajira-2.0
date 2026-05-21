from django.shortcuts import render
from django.utils.dateparse import parse_datetime, parse_date
from .models import Espacio, Reserva
from django.db.models import Count
from datetime import datetime

def home(request):
    return render(request, 'reservas/home.html')

def consulta_disponibilidad(request):
    espacios = Espacio.objects.all()
    resultado = None
    
    if request.method == 'POST':
        espacio_id = request.POST.get('espacio')
        inicio_str = request.POST.get('inicio')
        fin_str = request.POST.get('fin')
        
        if espacio_id and inicio_str and fin_str:
            inicio = parse_datetime(inicio_str)
            fin = parse_datetime(fin_str)
            espacio = Espacio.objects.get(id=espacio_id)
            
            # Buscar conflictos
            conflictos = Reserva.objects.filter(
                espacio=espacio,
                estado='APROBADA',
                fecha_hora_inicio__lt=fin,
                fecha_hora_fin__gt=inicio
            )
            
            if conflictos.exists():
                resultado = {'disponible': False, 'espacio': espacio}
            else:
                resultado = {'disponible': True, 'espacio': espacio}
                
    return render(request, 'reservas/disponibilidad.html', {
        'espacios': espacios,
        'resultado': resultado
    })

def agenda_diaria(request):
    fecha_str = request.GET.get('fecha', datetime.now().strftime('%Y-%m-%d'))
    fecha = parse_date(fecha_str)
    
    if fecha:
        reservas = Reserva.objects.filter(
            fecha_hora_inicio__date=fecha,
            estado='APROBADA'
        ).order_by('fecha_hora_inicio')
    else:
        reservas = []
        
    return render(request, 'reservas/agenda.html', {
        'reservas': reservas,
        'fecha': fecha_str
    })

def reporte_reservas(request):
    por_estado = Reserva.objects.values('estado').annotate(total=Count('id'))
    por_espacio = Reserva.objects.values('espacio__nombre').annotate(total=Count('id'))
    
    return render(request, 'reservas/reporte.html', {
        'por_estado': por_estado,
        'por_espacio': por_espacio
    })
