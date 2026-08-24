from unittest.mock import Mock, patch

from django.test import TestCase
from django.urls import reverse

from .models import Colaborador, Contacto, Noticia, OfertaMes, Producto


class ContactoTests(TestCase):
    @patch("sitio.views.send_mail", return_value=1)
    def test_contacto_se_guarda_y_envia_correo(self, enviar):
        respuesta = self.client.post(
            reverse("guardar_contacto"),
            {
                "nombre": "Mateo Alvarez",
                "email": "mateo@example.com",
                "mensaje": "Mensaje de prueba para el formulario.",
            },
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Contacto.objects.count(), 1)
        enviar.assert_called_once()


class InicioTests(TestCase):
    def test_inicio_muestra_catalogo_ofertas_noticias_y_colaboradores(self):
        producto = Producto.objects.create(
            nombre="Martillo de acero",
            categoria="Herramientas",
            descripcion="Martillo resistente para trabajos de construccion.",
            precio="12.50",
            stock=8,
            imagen_url="https://example.com/martillo.jpg",
        )
        OfertaMes.objects.create(
            producto=producto,
            descripcion="Oferta especial para trabajos de remodelacion.",
            precio_anterior="12.50",
            precio_oferta="9.99",
        )
        Noticia.objects.create(
            fecha="2026-07-20",
            titulo="Nueva promocion en herramientas",
            contenido="Promocion disponible durante este mes.",
            imagen_url="https://example.com/noticia.jpg",
        )
        Colaborador.objects.create(
            nombre="Laura Perez",
            cargo="Asesora comercial",
            foto_url="https://example.com/laura.jpg",
        )

        respuesta = self.client.get(reverse("inicio"))

        self.assertContains(respuesta, "Martillo de acero")
        self.assertContains(respuesta, "Oferta especial para trabajos de remodelacion.")
        self.assertContains(respuesta, "Nueva promocion en herramientas")
        self.assertContains(respuesta, "Laura Perez")


class ClimaTests(TestCase):
    @patch("sitio.views.requests.get")
    def test_clima_retorna_los_cuatro_datos(self, get_mock):
        api = Mock()
        api.raise_for_status.return_value = None
        api.json.return_value = {
            "name": "Quito",
            "sys": {"country": "EC"},
            "main": {"temp": 18.5, "humidity": 70},
            "weather": [{"description": "nubes dispersas"}],
            "wind": {"speed": 3.2},
        }
        get_mock.return_value = api

        with self.settings(OPENWEATHER_API_KEY="clave-de-prueba"):
            respuesta = self.client.get(reverse("api_clima"), {"ciudad": "Quito"})

        datos = respuesta.json()
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(datos["temperatura"], 18.5)
        self.assertEqual(datos["humedad"], 70)
        self.assertEqual(datos["descripcion"], "nubes dispersas")
        self.assertEqual(datos["viento"], 3.2)
