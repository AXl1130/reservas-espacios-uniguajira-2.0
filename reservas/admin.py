from django.contrib import admin
from .models import TipoEspacio, Espacio, Reserva, DetalleReserva, ServicioAdicional

class DetalleReservaInline(admin.StackedInline):
    model = DetalleReserva
    can_delete = False
    verbose_name_plural = 'Detalles de la Reserva'

@admin.register(TipoEspacio)
class TipoEspacioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Espacio)
class EspacioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'capacidad', 'tipo_espacio')
    list_filter = ('tipo_espacio',)
    search_fields = ('nombre', 'ubicacion')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'espacio', 'fecha_hora_inicio', 'fecha_hora_fin', 'estado')
    list_filter = ('estado', 'espacio', 'fecha_hora_inicio')
    search_fields = ('usuario__username', 'espacio__nombre')
    inlines = (DetalleReservaInline,)
    
    actions = ['aprobar_reservas', 'cancelar_reservas']

    def aprobar_reservas(self, request, queryset):
        queryset.update(estado='APROBADA')
    aprobar_reservas.short_description = "Aprobar reservas seleccionadas"

    def cancelar_reservas(self, request, queryset):
        queryset.update(estado='CANCELADA')
    cancelar_reservas.short_description = "Cancelar reservas seleccionadas"

@admin.register(ServicioAdicional)
class ServicioAdicionalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    filter_horizontal = ('reservas',)
