from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("contacto/guardar/", views.guardar_contacto, name="guardar_contacto"),
    path("api/clima/", views.api_clima, name="api_clima"),
]
