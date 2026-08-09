from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contacto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=150)),
                ("mensaje", models.TextField()),
            ],
            options={
                "verbose_name": "Contacto",
                "verbose_name_plural": "Contactos",
                "db_table": "Contacto",
            },
        ),
    ]
