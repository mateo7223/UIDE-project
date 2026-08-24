from django.db import models


class Contacto(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField(max_length=150)
    mensaje = models.TextField()

    class Meta:
        db_table = "Contacto"
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"

    def __str__(self):
        return f"{self.nombre} - {self.email}"


class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    categoria = models.CharField(max_length=80)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen_url = models.URLField("URL de imagen", max_length=500)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "Producto"
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["categoria", "nombre"]

    def __str__(self):
        return self.nombre


class OfertaMes(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="ofertas",
    )
    descripcion = models.TextField()
    precio_anterior = models.DecimalField(max_digits=8, decimal_places=2)
    precio_oferta = models.DecimalField(max_digits=8, decimal_places=2)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = "OfertaMes"
        verbose_name = "Oferta del mes"
        verbose_name_plural = "Ofertas del mes"
        ordering = ["producto__nombre"]

    def __str__(self):
        return f"{self.producto.nombre} - ${self.precio_oferta}"


class Noticia(models.Model):
    fecha = models.DateField()
    titulo = models.CharField(max_length=150)
    contenido = models.TextField()
    imagen_url = models.URLField("URL de imagen", max_length=500)
    publicada = models.BooleanField(default=True)

    class Meta:
        db_table = "Noticia"
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ["-fecha"]

    def __str__(self):
        return self.titulo


class Colaborador(models.Model):
    nombre = models.CharField(max_length=120)
    cargo = models.CharField(max_length=120)
    foto_url = models.URLField("URL de foto", max_length=500)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "Colaborador"
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"
        ordering = ["orden", "nombre"]

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"
