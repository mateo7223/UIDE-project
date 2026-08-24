from django.contrib import admin

from .models import Colaborador, Contacto, Noticia, OfertaMes, Producto


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "email")
    search_fields = ("nombre", "email", "mensaje")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "categoria", "precio", "stock", "activo")
    list_filter = ("categoria", "activo")
    search_fields = ("nombre", "categoria", "descripcion")


@admin.register(OfertaMes)
class OfertaMesAdmin(admin.ModelAdmin):
    list_display = ("id", "producto", "precio_anterior", "precio_oferta", "activa")
    list_filter = ("activa",)
    search_fields = ("producto__nombre", "descripcion")


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "titulo", "publicada")
    list_filter = ("publicada", "fecha")
    search_fields = ("titulo", "contenido")


@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "cargo", "orden")
    search_fields = ("nombre", "cargo")
