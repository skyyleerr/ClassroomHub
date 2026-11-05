# ClassroomHub

Portal web de recursos de aprendizaje construido con Django como primera aplicación del Laboratorio 06 (Python, programa ADSO). Muestra tres páginas navegables que comparten una plantilla base y datos de ejemplo enviados desde las vistas.

## Versiones

- Python 3.12 – 3.15 (desarrollado y probado con Python 3.13)
- Django 6.1.3 (fijado en `requirements.txt`)

> Con Python 3.10 u 3.11 usa `Django==5.2.19` en lugar de `Django==6.1.3`.

## Instalación

```bash
python -m venv .venv
```

Activar el entorno:

- Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
- Linux/macOS: `source .venv/bin/activate`

Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

## Verificación y ejecución

```bash
python manage.py check
python manage.py test pages
python manage.py runserver
```

Abrir http://127.0.0.1:8000/ en el navegador. Si el puerto está ocupado: `python manage.py runserver 8001`.

## Rutas públicas

| Ruta | Nombre | Descripción |
|---|---|---|
| `/` | `pages:home` | Página principal con mensaje de bienvenida |
| `/resources/` | `pages:resources` | Lista de recursos con su estado de disponibilidad |
| `/about/` | `pages:about` | Propósito del proyecto |

Cualquier otra dirección responde `404 Not Found`.

## Estructura

```text
config/   configuración del proyecto (settings.py, urls.py)
pages/    aplicación: urls.py, views.py, tests.py y templates/pages/
```

Las plantillas `home.html`, `resources.html` y `about.html` heredan de `base.html`, y la navegación usa nombres de ruta con `{% url %}`.

## Pruebas

`python manage.py test pages` ejecuta cinco pruebas automatizadas: respuesta y plantilla de cada página, enlace de navegación construido con `reverse()` y respuesta 404 para una ruta inexistente.

## Funcionalidades pendientes

Este laboratorio no incluye base de datos propia, modelos, migraciones, formularios, autenticación ni operaciones CRUD. Los recursos son datos de ejemplo definidos en `pages/views.py`. Se abordarán en el Laboratorio 7 (modelos, ORM, migraciones y administrador de Django).
