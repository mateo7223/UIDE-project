from unittest.mock import Mock, patch

from django.test import TestCase
from django.urls import reverse

from .models import Contacto


class ContactoTests(TestCase):
    @patch('contacto.views.send_mail', return_value=1)
    def test_guarda_contacto_y_envia_acuse(self, send_mail_mock):
        respuesta = self.client.post(
            reverse('contacto'),
            {
                'nombre': 'Mateo',
                'email': 'mateo@example.com',
                'mensaje': 'Mensaje de prueba',
            },
            follow=True,
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Contacto.objects.count(), 1)
        send_mail_mock.assert_called_once()

    @patch('contacto.views.requests.get')
    def test_clima_muestra_cuatro_datos(self, get_mock):
        respuesta_api = Mock()
        respuesta_api.raise_for_status.return_value = None
        respuesta_api.json.return_value = {
            'name': 'Quito',
            'sys': {'country': 'EC'},
            'main': {'temp': 18.5, 'humidity': 70},
            'weather': [{'description': 'nubes dispersas'}],
            'wind': {'speed': 3.1},
        }
        get_mock.return_value = respuesta_api

        with self.settings(OPENWEATHER_API_KEY='clave-prueba'):
            respuesta = self.client.get(reverse('clima'), {'ciudad': 'Quito'})

        self.assertContains(respuesta, '18.5')
        self.assertContains(respuesta, '70')
        self.assertContains(respuesta, 'nubes dispersas')
        self.assertContains(respuesta, '3.1')
