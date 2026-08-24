# Materials Fadrell - Contacto + Clima

Se tomó como base la web original de Materials Fadrell y se integraron las funcionalidades del Aprendizaje Autónomo 2.

## Funcionalidades agregadas

### Sitio web del emprendimiento
- Menú de una sola página con **Home**, **Empresa**, **Productos**, **Oferta del mes**, **Localización**, **Contacto**, **Noticias** y **Clima**.
- Home con información comercial de Materials Fadrell.
- Empresa con misión, visión, valores, organigrama, fotos y cargos de colaboradores.
- Localización visible con dirección, teléfono, correo y mapa visual.
- Colores e imágenes acordes al emprendimiento ferretero.

### Productos, ofertas y noticias desde base de datos
- Tabla `Producto`: nombre, categoría, descripción, precio, stock, imagen y estado activo.
- Tabla `OfertaMes`: producto relacionado, descripción, precio anterior, precio de oferta y estado activo.
- Tabla `Noticia`: fecha, título, contenido, imagen y estado de publicación.
- Tabla `Colaborador`: nombre, cargo, foto y orden.
- La página principal consulta estas tablas con Django ORM y muestra la información en el front end.
- La migración `0002_catalogo_ofertas_noticias_colaboradores.py` carga datos iniciales para que el sitio tenga contenido al instalarse.

### Paso 1 - Contacto E/R
- Tabla de base de datos llamada `Contacto`.
- Campos: `nombre`, `email` y `mensaje`.
- Botón **Guardar**.
- Guardado real con Django ORM y SQLite.
- Consulta de registros desde `/admin/`.
- Envío de acuse de recibido al correo ingresado.
- Configuración SMTP compatible con **Brevo** mediante variables del archivo `.env`.
- Script `subir_ftp.py` que utiliza el módulo `ftplib`.

### Paso 2 - Clima
- Nueva opción **Clima** en el menú.
- Consulta a OpenWeatherMap desde el backend.
- La API KEY no se expone en JavaScript.
- Muestra:
  - Temperatura.
  - Humedad.
  - Descripción del clima.
  - Viento.
- Permite consultar otras ciudades.

## Tu archivo .env

El proyecto NO reemplaza tus datos. Coloca tu `.env` en la raíz, junto a `manage.py`.

El código reconoce estas variables:

```env
OPENWEATHER_API_KEY=...
OPENWEATHER_DEFAULT_CITY=Quito

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-relay.brevo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
DEFAULT_FROM_EMAIL=...

FTP_HOST=...
FTP_PORT=21
FTP_USER=...
FTP_PASSWORD=...
FTP_REMOTE_DIR=...
FTP_USE_TLS=False
```

También se acepta `OPENWEATHERMAP_API_KEY` como nombre alternativo de la clave del clima.

## Ejecutar

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Instalar:

```bash
pip install -r requirements.txt
```

Base de datos:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Ejecutar:

```bash
python manage.py runserver
```

Abrir:

```text
http://127.0.0.1:8000/
```

Panel para comprobar la tabla Contacto:

```text
http://127.0.0.1:8000/admin/
```

## Probar contacto

1. Abra la sección **Contacto**.
2. Ingrese Nombre, E-Mail y Mensaje.
3. Presione **Guardar**.
4. El registro queda almacenado en la tabla `Contacto`.
5. Brevo envía el acuse de recibido al correo del usuario.
6. Compruebe el registro en `/admin/`.

## Probar clima

1. Abra **Clima** en el menú.
2. Escriba Quito u otra ciudad.
3. Presione **Consultar clima**.
4. Deben aparecer temperatura, humedad, descripción y viento.

## Subir al FTP con ftplib

Con tus datos FTP ya colocados en `.env`:

```bash
python subir_ftp.py
```

## Subir a GitLab

```bash
git init
git add .
git commit -m "AA2 - Contacto y reporteador de clima"
git branch -M main
git remote add origin URL_DE_TU_PROYECTO_GITLAB
git push -u origin main
```

El archivo `.env` está excluido por `.gitignore` para no publicar tus claves.

## Pruebas

```bash
python manage.py test
```

El proyecto incluye pruebas del guardado del contacto/correo y de los cuatro datos requeridos del clima.
