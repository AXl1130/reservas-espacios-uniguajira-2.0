from django import forms
from django.contrib.auth.models import User
from .models import Reserva, Espacio, ServicioAdicional

class ReservaForm(forms.ModelForm):
    motivo = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        label='Motivo de la reserva'
    )
    observaciones_admin = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        label='Observaciones administrativas'
    )
    servicios_adicionales = forms.ModelMultipleChoiceField(
        required=False,
        queryset=ServicioAdicional.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        label='Servicios adicionales'
    )

    class Meta:
        model = Reserva
        fields = ['usuario', 'espacio', 'fecha_hora_inicio', 'fecha_hora_fin', 'estado']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'espacio': forms.Select(attrs={'class': 'form-select'}),
            'fecha_hora_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_hora_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
