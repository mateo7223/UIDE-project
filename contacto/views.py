import requests
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import ContactoForm


def inicio(request):
    return render(request, 'inicio.html')


def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            registro = form.save()

            asunto = 'Confirmación de mensaje recibido'
            cuerpo = (
                f'Hola {registro.nombre},\n\n'
                'Hemos recibido correctamente su mensaje. '
                'Gracias por ponerse en contacto con nosotros.\n\n'
                'Este correo es un acuse de recibido generado automáticamente.'
            )

            try:
                send_mail(
                    asunto,
                    cuerpo,
                    settings.DEFAULT_FROM_EMAIL,
                    [registro.email],
                    fail_silently=False,
                )
                messages.success(
                    request,
                    'Su mensaje fue guardado y se envió el acuse de recibido a su correo.'
                )
            except Exception:
                messages.warning(
                    request,
                    'El mensaje se guardó en la base de datos, pero no se pudo enviar el correo. '
                    'Revise la configuración SMTP del archivo .env.'
                )
            return redirect('contacto')
    else:
        form = ContactoForm()

    return render(request, 'contacto/contacto.html', {'form': form})


def clima(request):
    ciudad = request.GET.get('ciudad', settings.OPENWEATHER_DEFAULT_CITY).strip() or 'Quito'
    clima_actual = None
    error = None

    if not settings.OPENWEATHER_API_KEY:
        error = 'Falta configurar OPENWEATHER_API_KEY en el archivo .env.'
    else:
        try:
            respuesta = requests.get(
                'https://api.openweathermap.org/data/2.5/weather',
                params={
                    'q': ciudad,
                    'appid': settings.OPENWEATHER_API_KEY,
                    'units': 'metric',
                    'lang': 'es',
                },
                timeout=10,
            )
            respuesta.raise_for_status()
            datos = respuesta.json()

            clima_actual = {
                'ciudad': datos.get('name', ciudad),
                'pais': datos.get('sys', {}).get('country', ''),
                'temperatura': datos.get('main', {}).get('temp'),
                'humedad': datos.get('main', {}).get('humidity'),
                'descripcion': (datos.get('weather') or [{}])[0].get('description', 'Sin descripción'),
                'viento': datos.get('wind', {}).get('speed'),
            }
        except requests.RequestException:
            error = 'No fue posible consultar el clima. Verifique la ciudad, la conexión y la API KEY.'

    return render(
        request,
        'contacto/clima.html',
        {'clima': clima_actual, 'error': error, 'ciudad': ciudad},
    )
