from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Espacio, TipoEspacio


class CrearEspacioTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            password='12345678'
        )
        self.tipo_default = TipoEspacio.objects.create(
            nombre='Salón',
            descripcion='Tipo predeterminado'
        )

    def test_puede_crear_espacio_con_tipo_nuevo(self):
        self.client.login(username='admin', password='12345678')

        response = self.client.post(
            reverse('crear_espacio'),
            {
                'nombre': 'Laboratorio 101',
                'tipo_espacio': '',
                'nuevo_tipo': 'Laboratorio',
                'ubicacion': 'Bloque B',
                'capacidad': '25'
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Espacio.objects.filter(nombre='Laboratorio 101').exists())
        self.assertTrue(TipoEspacio.objects.filter(nombre='Laboratorio').exists())
