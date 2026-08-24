from decimal import Decimal
from datetime import date

from django.db import migrations, models
import django.db.models.deletion


def cargar_datos_iniciales(apps, schema_editor):
    Producto = apps.get_model("sitio", "Producto")
    OfertaMes = apps.get_model("sitio", "OfertaMes")
    Noticia = apps.get_model("sitio", "Noticia")
    Colaborador = apps.get_model("sitio", "Colaborador")

    productos = [
        {
            "nombre": "Taladro electrico profesional",
            "categoria": "Herramientas",
            "descripcion": "Taladro de 650 W con velocidad regulable, mandril de 13 mm y garantia de doce meses.",
            "precio": Decimal("79.99"),
            "stock": 15,
            "imagen_url": "https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&w=900&q=80",
        },
        {
            "nombre": "Pintura interior blanca",
            "categoria": "Pinturas",
            "descripcion": "Pintura lavable de acabado mate para interiores, presentacion de 4 litros.",
            "precio": Decimal("28.50"),
            "stock": 24,
            "imagen_url": "https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&w=900&q=80",
        },
        {
            "nombre": "Juego de destornilladores",
            "categoria": "Herramientas",
            "descripcion": "Set de seis destornilladores con mango ergonomico y puntas resistentes.",
            "precio": Decimal("18.75"),
            "stock": 32,
            "imagen_url": "https://images.unsplash.com/photo-1586864387967-d02ef85d93e8?auto=format&fit=crop&w=900&q=80",
        },
        {
            "nombre": "Cable electrico THHN",
            "categoria": "Electricidad",
            "descripcion": "Rollo de cable electrico de 100 metros para instalaciones residenciales.",
            "precio": Decimal("35.00"),
            "stock": 18,
            "imagen_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=900&q=80",
        },
        {
            "nombre": "Llave ajustable para tuberia",
            "categoria": "Plomeria",
            "descripcion": "Llave de acero reforzado para trabajos de instalacion y mantenimiento.",
            "precio": Decimal("22.40"),
            "stock": 10,
            "imagen_url": "https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?auto=format&fit=crop&w=900&q=80",
        },
        {
            "nombre": "Cemento de uso general",
            "categoria": "Construccion",
            "descripcion": "Saco de cemento de 50 kg para mezclas, reparaciones y obras civiles.",
            "precio": Decimal("9.80"),
            "stock": 60,
            "imagen_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=900&q=80",
        },
    ]

    productos_creados = {
        datos["nombre"]: Producto.objects.create(**datos)
        for datos in productos
    }

    OfertaMes.objects.create(
        producto=productos_creados["Taladro electrico profesional"],
        descripcion="Promocion especial para obras y mantenimiento: incluye brocas basicas y asesoria de uso.",
        precio_anterior=Decimal("79.99"),
        precio_oferta=Decimal("59.99"),
    )
    OfertaMes.objects.create(
        producto=productos_creados["Pintura interior blanca"],
        descripcion="Oferta recomendada para renovaciones de habitaciones, oficinas y locales comerciales.",
        precio_anterior=Decimal("28.50"),
        precio_oferta=Decimal("22.90"),
    )

    Noticia.objects.bulk_create(
        [
            Noticia(
                fecha=date(2026, 7, 10),
                titulo="Nueva linea de herramientas electricas",
                contenido="Materials Fadrell incorporo equipos de alto rendimiento para perforacion, corte y mantenimiento.",
                imagen_url="https://images.unsplash.com/photo-1530124566582-a618bc2615dc?auto=format&fit=crop&w=900&q=80",
            ),
            Noticia(
                fecha=date(2026, 7, 5),
                titulo="Descuentos para contratistas",
                contenido="Los clientes que compran al por mayor pueden acceder a precios preferenciales en materiales seleccionados.",
                imagen_url="https://images.unsplash.com/photo-1541888946425-d81bb19240f5?auto=format&fit=crop&w=900&q=80",
            ),
            Noticia(
                fecha=date(2026, 7, 1),
                titulo="Entregas rapidas dentro de Quito",
                contenido="El emprendimiento fortalece su servicio de despacho para atender proyectos urgentes en diferentes sectores.",
                imagen_url="https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&w=900&q=80",
            ),
        ]
    )

    Colaborador.objects.bulk_create(
        [
            Colaborador(
                nombre="Mateo Alvarez",
                cargo="Gerente general",
                foto_url="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=500&q=80",
                orden=1,
            ),
            Colaborador(
                nombre="Daniela Rivas",
                cargo="Asesora de ventas",
                foto_url="https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=500&q=80",
                orden=2,
            ),
            Colaborador(
                nombre="Carlos Medina",
                cargo="Coordinador de bodega",
                foto_url="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=500&q=80",
                orden=3,
            ),
        ]
    )


def borrar_datos_iniciales(apps, schema_editor):
    Producto = apps.get_model("sitio", "Producto")
    OfertaMes = apps.get_model("sitio", "OfertaMes")
    Noticia = apps.get_model("sitio", "Noticia")
    Colaborador = apps.get_model("sitio", "Colaborador")

    OfertaMes.objects.all().delete()
    Producto.objects.all().delete()
    Noticia.objects.all().delete()
    Colaborador.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("sitio", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Producto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=120)),
                ("categoria", models.CharField(max_length=80)),
                ("descripcion", models.TextField()),
                ("precio", models.DecimalField(decimal_places=2, max_digits=8)),
                ("stock", models.PositiveIntegerField(default=0)),
                ("imagen_url", models.URLField(max_length=500, verbose_name="URL de imagen")),
                ("activo", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Producto",
                "verbose_name_plural": "Productos",
                "db_table": "Producto",
                "ordering": ["categoria", "nombre"],
            },
        ),
        migrations.CreateModel(
            name="Noticia",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha", models.DateField()),
                ("titulo", models.CharField(max_length=150)),
                ("contenido", models.TextField()),
                ("imagen_url", models.URLField(max_length=500, verbose_name="URL de imagen")),
                ("publicada", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Noticia",
                "verbose_name_plural": "Noticias",
                "db_table": "Noticia",
                "ordering": ["-fecha"],
            },
        ),
        migrations.CreateModel(
            name="Colaborador",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=120)),
                ("cargo", models.CharField(max_length=120)),
                ("foto_url", models.URLField(max_length=500, verbose_name="URL de foto")),
                ("orden", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "Colaborador",
                "verbose_name_plural": "Colaboradores",
                "db_table": "Colaborador",
                "ordering": ["orden", "nombre"],
            },
        ),
        migrations.CreateModel(
            name="OfertaMes",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("descripcion", models.TextField()),
                ("precio_anterior", models.DecimalField(decimal_places=2, max_digits=8)),
                ("precio_oferta", models.DecimalField(decimal_places=2, max_digits=8)),
                ("activa", models.BooleanField(default=True)),
                ("producto", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ofertas", to="sitio.producto")),
            ],
            options={
                "verbose_name": "Oferta del mes",
                "verbose_name_plural": "Ofertas del mes",
                "db_table": "OfertaMes",
                "ordering": ["producto__nombre"],
            },
        ),
        migrations.RunPython(cargar_datos_iniciales, borrar_datos_iniciales),
    ]
