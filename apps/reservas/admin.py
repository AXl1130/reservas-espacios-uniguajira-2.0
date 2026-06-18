from django.contrib import admin
from django.utils.html import format_html
from .models import TipoEspacio, Espacio, Reserva, DetalleReserva, ServicioAdicional

# ============================================================
# Personalización global del Admin
# ============================================================
admin.site.site_header  = "Panel de Reservas — Uniguajira"
admin.site.site_title   = "Admin Reservas Uniguajira"
admin.site.index_title  = "Gestión de Espacios y Reservas"

class DetalleReservaInline(admin.StackedInline):
    model = DetalleReserva
    can_delete = False
    verbose_name_plural = 'Detalles de la Reserva'
    fieldsets = (
        ('Información del detalle', {
            'fields': ('motivo', 'observaciones_admin'),
            'description': 'Complete los detalles adicionales de la reserva'
        }),
    )

@admin.register(TipoEspacio)
class TipoEspacioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'total_espacios')
    search_fields = ('nombre',)

    def total_espacios(self, obj):
        count = obj.espacios.count()
        return format_html(
            '<span style="background:#004a9915;color:#004a99;padding:3px 10px;'
            'border-radius:12px;font-weight:500;">{} espacio{}</span>',
            count, 's' if count != 1 else ''
        )
    total_espacios.short_description = 'Espacios'

@admin.register(Espacio)
class EspacioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'capacidad_badge', 'tipo_espacio')
    list_filter = ('tipo_espacio',)
    search_fields = ('nombre', 'ubicacion')

    def capacidad_badge(self, obj):
        return format_html(
            '<span style="background:#19875415;color:#198754;padding:3px 10px;'
            'border-radius:12px;font-weight:500;">'
            '{} personas</span>', obj.capacidad
        )
    capacidad_badge.short_description = 'Capacidad'

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'espacio', 'horario', 'estado_badge')
    list_filter = ('estado', 'espacio', 'fecha_hora_inicio')
    search_fields = ('usuario__username', 'espacio__nombre', 'usuario__first_name')
    inlines = (DetalleReservaInline,)
    date_hierarchy = 'fecha_hora_inicio'

    fieldsets = (
        ('Datos principales', {
            'fields': ('usuario', 'espacio', 'estado'),
        }),
        ('Horario', {
            'fields': ('fecha_hora_inicio', 'fecha_hora_fin'),
        }),
    )

    def horario(self, obj):
        return format_html(
            '{} → {}',
            obj.fecha_hora_inicio.strftime('%d/%m/%Y %H:%M'),
            obj.fecha_hora_fin.strftime('%H:%M')
        )
    horario.short_description = 'Horario'
    horario.admin_order_field = 'fecha_hora_inicio'

    def estado_badge(self, obj):
        colores = {
            'APROBADA':  ('#198754', '#d1e7dd'),
            'PENDIENTE': ('#fd7e14', '#fff3cd'),
            'CANCELADA': ('#dc3545', '#f8d7da'),
        }
        color, bg = colores.get(obj.estado, ('#6c757d', '#e9ecef'))
        return format_html(
            '<span style="background:{};color:{};padding:4px 12px;'
            'border-radius:12px;font-weight:500;font-size:0.85em;">'
            '{}</span>', bg, color, obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'

    actions = ['aprobar_reservas', 'cancelar_reservas']

    def aprobar_reservas(self, request, queryset):
        actualizadas = queryset.update(estado='APROBADA')
        self.message_user(request, f'{actualizadas} reserva(s) aprobada(s) correctamente.')
    aprobar_reservas.short_description = "✅  Aprobar reservas seleccionadas"

    def cancelar_reservas(self, request, queryset):
        actualizadas = queryset.update(estado='CANCELADA')
        self.message_user(request, f'{actualizadas} reserva(s) cancelada(s).')
    cancelar_reservas.short_description = "❌  Cancelar reservas seleccionadas"

    class Media:
        css = {
            'all': ('css/admin_personalizado.css',)
        }

@admin.register(ServicioAdicional)
class ServicioAdicionalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'total_reservas')
    filter_horizontal = ('reservas',)

    def total_reservas(self, obj):
        count = obj.reservas.count()
        return format_html(
            '<span style="background:#0dcaf015;color:#0d6efd;padding:3px 10px;'
            'border-radius:12px;font-weight:500;">'
            '{} reserva{}</span>', count, 's' if count != 1 else ''
        )
    total_reservas.short_description = 'Vinculado a'
