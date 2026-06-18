from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class TipoEspacio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Espacio(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    capacidad = models.IntegerField()
    tipo_espacio = models.ForeignKey(TipoEspacio, on_delete=models.CASCADE, related_name='espacios')

    def __str__(self):
        return f"{self.nombre} ({self.ubicacion})"

class Reserva(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE, related_name='reservas')
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    def clean(self):
        # Validar solapamientos
        solapamientos = Reserva.objects.filter(
            espacio=self.espacio,
            estado='APROBADA',
            fecha_hora_inicio__lt=self.fecha_hora_fin,
            fecha_hora_fin__gt=self.fecha_hora_inicio
        ).exclude(pk=self.pk)

        if solapamientos.exists():
            raise ValidationError('Ya existe una reserva aprobada para este espacio en el horario seleccionado.')

        if self.fecha_hora_inicio >= self.fecha_hora_fin:
            raise ValidationError('La fecha de inicio debe ser anterior a la fecha de fin.')

    def __str__(self):
        return f"Reserva de {self.usuario} en {self.espacio} ({self.fecha_hora_inicio})"

class DetalleReserva(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='detalle')
    motivo = models.TextField()
    observaciones_admin = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Detalle de la {self.reserva}"

class ServicioAdicional(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    reservas = models.ManyToManyField(Reserva, related_name='servicios_adicionales', blank=True)

    def __str__(self):
        return self.nombre
