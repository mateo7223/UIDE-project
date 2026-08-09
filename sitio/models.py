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
