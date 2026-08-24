import requests

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .forms import ContactoForm
from .models import Colaborador, Noticia, OfertaMes, Producto


def inicio(request):
    productos = [
        {
            "id": producto.id,
            "nombre": producto.nombre,
            "categoria": producto.categoria,
            "descripcion": producto.descripcion,
            "precio": float(producto.precio),
            "stock": producto.stock,
            "imagen": producto.imagen_url,
        }
        for producto in Producto.objects.filter(activo=True)
    ]
    ofertas = [
        {
            "id": oferta.id,
            "producto": oferta.producto.nombre,
            "categoria": oferta.producto.categoria,
            "descripcion": oferta.descripcion,
            "precio_anterior": float(oferta.precio_anterior),
            "precio_oferta": float(oferta.precio_oferta),
            "imagen": oferta.producto.imagen_url,
        }
        for oferta in OfertaMes.objects.select_related("producto").filter(activa=True)
    ]
    noticias = [
        {
            "fecha": noticia.fecha.strftime("%d/%m/%Y"),
            "titulo": noticia.titulo,
            "contenido": noticia.contenido,
            "imagen": noticia.imagen_url,
        }
        for noticia in Noticia.objects.filter(publicada=True)
    ]
    colaboradores = Colaborador.objects.all()

    return render(
        request,
        "index.html",
        {
            "ciudad_inicial": settings.OPENWEATHER_DEFAULT_CITY,
            "productos": productos,
            "ofertas": ofertas,
            "noticias": noticias,
            "colaboradores": colaboradores,
        },
    )


@require_POST
def guardar_contacto(request):
    form = ContactoForm(request.POST)

    if not form.is_valid():
        return JsonResponse(
            {
                "ok": False,
                "mensaje": "Revise los campos del formulario.",
                "errores": form.errors.get_json_data(),
            },
            status=400,
        )

    contacto = form.save()

    asunto = "Confirmación de mensaje recibido - Materials Fadrell"
    cuerpo = (
        f"Hola {contacto.nombre},\n\n"
        "Hemos recibido correctamente tu mensaje en Materials Fadrell. "
        "Gracias por comunicarte con nosotros.\n\n"
        "Este correo es un acuse de recibido automático."
    )

    correo_enviado = True
    detalle_correo = ""

    try:
        send_mail(
            asunto,
            cuerpo,
            settings.DEFAULT_FROM_EMAIL,
            [contacto.email],
            fail_silently=False,
        )
    except Exception as exc:
        correo_enviado = False
        detalle_correo = str(exc)

    return JsonResponse(
        {
            "ok": True,
            "guardado": True,
            "correo_enviado": correo_enviado,
            "mensaje": (
                "Tu mensaje fue guardado y el acuse de recibido fue enviado a tu correo."
                if correo_enviado
                else "Tu mensaje fue guardado, pero no se pudo enviar el correo de confirmación."
            ),
            "detalle_correo": detalle_correo if settings.DEBUG else "",
        }
    )


@require_GET
def api_clima(request):
    ciudad = (
        request.GET.get("ciudad", "").strip()
        or settings.OPENWEATHER_DEFAULT_CITY
        or "Quito"
    )

    if not settings.OPENWEATHER_API_KEY:
        return JsonResponse(
            {
                "ok": False,
                "mensaje": "No se encontró OPENWEATHER_API_KEY en el archivo .env.",
            },
            status=500,
        )

    try:
        respuesta = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": ciudad,
                "appid": settings.OPENWEATHER_API_KEY,
                "units": "metric",
                "lang": "es",
            },
            proxies={"http": "", "https": ""},
            timeout=10,
        )
        respuesta.raise_for_status()
        datos = respuesta.json()
    except requests.HTTPError:
        codigo = getattr(respuesta, "status_code", 500)
        if codigo == 404:
            mensaje = "No se encontró la ciudad indicada."
        elif codigo == 401:
            mensaje = "La API KEY de OpenWeatherMap no es válida o todavía no está activa."
        else:
            mensaje = "OpenWeatherMap devolvió un error al consultar el clima."
        return JsonResponse({"ok": False, "mensaje": mensaje}, status=502)
    except requests.RequestException:
        return JsonResponse(
            {
                "ok": False,
                "mensaje": "No fue posible conectarse con OpenWeatherMap.",
            },
            status=502,
        )

    return JsonResponse(
        {
            "ok": True,
            "ciudad": datos.get("name", ciudad),
            "pais": datos.get("sys", {}).get("country", ""),
            "temperatura": datos.get("main", {}).get("temp"),
            "humedad": datos.get("main", {}).get("humidity"),
            "descripcion": (datos.get("weather") or [{}])[0].get(
                "description", "Sin descripción"
            ),
            "viento": datos.get("wind", {}).get("speed"),
        }
    )
