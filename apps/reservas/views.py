from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime, parse_date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Espacio, Reserva, DetalleReserva
from .forms import ReservaForm
from django.db.models import Count
from datetime import datetime

def home(request):
    return render(request, 'reservas/home.html')

@login_required
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

@login_required
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

@login_required
def reporte_reservas(request):
    por_estado = Reserva.objects.values('estado').annotate(total=Count('id'))
    por_espacio = Reserva.objects.values('espacio__nombre').annotate(total=Count('id'))

    return render(request, 'reservas/reporte.html', {
        'por_estado': por_estado,
        'por_espacio': por_espacio
    })

@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            try:
                reserva.clean()
            except Exception as e:
                form.add_error(None, e)
                return render(request, 'reservas/crear_reserva.html', {'form': form})

            reserva.save()
            DetalleReserva.objects.create(
                reserva=reserva,
                motivo=form.cleaned_data['motivo'],
                observaciones_admin=form.cleaned_data.get('observaciones_admin', '')
            )
            reserva.servicios_adicionales.set(form.cleaned_data['servicios_adicionales'])
            messages.success(request, 'Reserva creada exitosamente.')
            return redirect('crear_reserva')
    else:
        form = ReservaForm()

    return render(request, 'reservas/crear_reserva.html', {'form': form})

# ============================================================
# Gestión de Espacios — Interfaz amigable (no admin)
# ============================================================
from .models import TipoEspacio

@login_required
def mis_espacios(request):
    """Lista de espacios con diseño intuitivo para cualquier persona"""
    espacios = Espacio.objects.all().order_by('tipo_espacio__nombre', 'nombre')
    tipos = TipoEspacio.objects.all()
    
    total_espacios = espacios.count()
    total_capacidad = sum(e.capacidad for e in espacios)
    
    return render(request, 'reservas/mis_espacios.html', {
        'espacios': espacios,
        'tipos': tipos,
        'total_espacios': total_espacios,
        'total_capacidad': total_capacidad,
    })

@login_required
def crear_espacio(request):
    """Formulario SIMPLE para crear un espacio — paso a paso guiado"""
    tipos = TipoEspacio.objects.all()
    if not tipos.exists():
        for nombre in ['Salón', 'Laboratorio', 'Auditorio', 'Oficina']:
            TipoEspacio.objects.get_or_create(nombre=nombre)
        tipos = TipoEspacio.objects.all()
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        tipo_id = request.POST.get('tipo_espacio')
        nuevo_tipo = request.POST.get('nuevo_tipo', '').strip()
        ubicacion = request.POST.get('ubicacion', '').strip()
        capacidad = request.POST.get('capacidad', '')
        
        errores = []
        
        if not nombre:
            errores.append('El nombre del espacio es obligatorio.')
        if not tipo_id and not nuevo_tipo:
            errores.append('Debe seleccionar un tipo de espacio o crear uno nuevo.')
        if not ubicacion:
            errores.append('La ubicación es obligatoria.')
        if not capacidad or not capacidad.isdigit() or int(capacidad) <= 0:
            errores.append('La capacidad debe ser un número positivo.')
        
        if not errores:
            try:
                if tipo_id:
                    tipo = TipoEspacio.objects.get(id=int(tipo_id))
                else:
                    tipo, created = TipoEspacio.objects.get_or_create(
                        nombre__iexact=nuevo_tipo,
                        defaults={'nombre': nuevo_tipo}
                    )
                Espacio.objects.create(
                    nombre=nombre,
                    tipo_espacio=tipo,
                    ubicacion=ubicacion,
                    capacidad=int(capacidad)
                )
                messages.success(request, f'¡Espacio "{nombre}" creado exitosamente! 🎉')
                return redirect('mis_espacios')
            except Exception as e:
                errores.append(f'Error al crear: {str(e)}')
        
        for error in errores:
            messages.error(request, error)
    
    return render(request, 'reservas/crear_espacio.html', {
        'tipos': tipos,
    })
