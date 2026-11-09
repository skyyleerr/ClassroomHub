# ClassroomHub

Portal web de recursos de aprendizaje construido con Django (programa ADSO, laboratorios de Python). El Laboratorio 06 creó las tres páginas con plantillas compartidas; el Laboratorio 07 sustituye la lista de recursos escrita en `views.py` por un catálogo **persistente en MySQL o MariaDB**, administrable desde Django Admin; el Laboratorio 08 añade **registro, inicio y cierre de sesión, panel con contador de sesión y revisión protegida por grupo y permiso**; el Laboratorio 09 añade **CRUD de recursos desde páginas propias (ModelForm + vistas genéricas) protegido por permisos**.

## Requisitos

- Python 3.12 – 3.15 (probado con Python 3.13)
- Django 6.1.3, `mysqlclient` y `python-dotenv` (fijados en `requirements.txt`)
- Servidor **MariaDB 10.11 o superior** o **MySQL 8.4 o superior** (mínimos para Django 6.1). Probado con MariaDB 10.11.
- Permisos para crear una base de datos y una cuenta SQL local.
- `mysqlclient` puede necesitar encabezados del cliente, compilador y `pkg-config` en Linux/macOS; en Windows suele instalarse ya compilado.

> Con Python 3.10 u 3.11 usa la rama Django 5.2 LTS (`Django==5.2.19`).

## 1. Preparar la base de datos

Con una cuenta administrativa del servidor (cambia la contraseña de ejemplo):

```sql
CREATE DATABASE IF NOT EXISTS classroom_hub
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'classroomhub_user'@'127.0.0.1'
    IDENTIFIED BY 'replace_with_a_private_password';

GRANT ALL PRIVILEGES ON classroom_hub.*      TO 'classroomhub_user'@'127.0.0.1';
GRANT ALL PRIVILEGES ON test_classroom_hub.* TO 'classroomhub_user'@'127.0.0.1';
```

La cuenta solo tiene permisos sobre dos esquemas: el de desarrollo y el descartable de pruebas. No se usa `root` ni se concede `ALL ON *.*`.

## 2. Instalar el proyecto

```bash
python -m venv .venv
```

Activar el entorno: Windows PowerShell `.\.venv\Scripts\Activate.ps1`, Linux/macOS `source .venv/bin/activate`.

```bash
python -m pip install -r requirements.txt
```

## 3. Configurar variables de entorno

Copia la plantilla y escribe tu contraseña real en `.env` (este archivo **no se versiona**):

```bash
cp .env.example .env        # Windows: copy .env.example .env
```

```dotenv
DB_NAME=classroom_hub
DB_USER=classroomhub_user
DB_PASSWORD=replace_with_a_private_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

## 4. Migraciones, administrador y arranque

```bash
python manage.py check
python manage.py migrate
python manage.py showmigrations pages
python manage.py createsuperuser
python manage.py runserver
```

`createsuperuser` te pide usuario y contraseña en la terminal: las credenciales **no se versionan**. El superusuario es una cuenta de Django, distinta del usuario SQL. Abre http://127.0.0.1:8000/admin/, crea categorías y recursos, y revisa http://127.0.0.1:8000/resources/.

## Cuentas, grupo y permisos (Laboratorio 08)

1. Entra a http://127.0.0.1:8000/admin/ con el superusuario.
2. En **Groups** crea el grupo `Catalog reviewers` y asígnale el permiso `pages | resource | Can view resource`.
3. En **Users** agrega al grupo a quien deba revisar el catálogo.

Alternativa por consola (`python manage.py shell`):

```python
from django.contrib.auth.models import Group, Permission
g, _ = Group.objects.get_or_create(name="Catalog reviewers")
g.permissions.add(Permission.objects.get(codename="view_resource", content_type__app_label="pages"))
```

Comportamiento esperado de `/resources/review/`: anónimo → redirige a login con `?next=`; autenticado sin permiso → `403`; miembro del grupo → `200`.

### Grupo `Catalog editors` (Laboratorio 09)

Crea un segundo grupo, **distinto** de `Catalog reviewers`, con los permisos `view_resource`, `add_resource`, `change_resource` y `delete_resource` de `pages | resource`. Desde Admin (Groups) o por consola:

```python
from django.contrib.auth.models import Group, Permission
codes = ["view_resource", "add_resource", "change_resource", "delete_resource"]
perms = Permission.objects.filter(content_type__app_label="pages", content_type__model="resource", codename__in=codes)
assert perms.count() == 4
g, _ = Group.objects.get_or_create(name="Catalog editors")
g.permissions.add(*perms)
```

Después, en Admin > Users, asigna el grupo **solo** a una cuenta de demostración. **El formulario público de registro no asigna grupos ni permisos**, y los editores no necesitan `is_staff`. Las categorías se siguen creando desde Admin (el `ModelForm` solo permite elegir categorías existentes).

## Rutas

| Ruta | Nombre | Acceso | Descripción |
|---|---|---|---|
| `/` | `pages:home` | público | Página principal |
| `/resources/` | `pages:resources` | público | Recursos consultados con el ORM; mensaje si el catálogo está vacío |
| `/resources/available/` | `pages:available_resources` | público | Solo recursos disponibles (reto adicional) |
| `/resources/new/` | `pages:resource-create` | permiso `pages.add_resource` | GET formulario / POST crea (redirige a `/resources/`) |
| `/resources/<pk>/` | `pages:resource-detail` | público | Detalle de un recurso (404 si no existe) |
| `/resources/<pk>/edit/` | `pages:resource-update` | permiso `pages.change_resource` | GET formulario con datos / POST actualiza la misma fila |
| `/resources/<pk>/delete/` | `pages:resource-delete` | permiso `pages.delete_resource` | GET solo confirma / POST elimina |
| `/resources/review/` | `pages:resource-review` | login + permiso `pages.view_resource` | Revisión del catálogo |
| `/about/` | `pages:about` | público | Propósito del proyecto |
| `/accounts/signup/` | `pages:signup` | público | Registro con `UserCreationForm` |
| `/accounts/login/` | `pages:login` | público | Inicio de sesión (`LoginView`) |
| `/accounts/logout/` | `pages:logout` | solo `POST` + CSRF | Cierre de sesión (`LogoutView`) |
| `/dashboard/` | `pages:dashboard` | login | Panel con contador de visitas guardado en la sesión |
| `/admin/` | — | staff | Django Admin |

Cualquier otra dirección responde `404`.

## Modelos

- `Category`: `name` (único), `description`.
- `Resource`: `title`, `description`, `available`, `resource_type`, `created_at` y `category` (`ForeignKey` con `related_name="resources"` y `on_delete=PROTECT`, por lo que no se puede borrar una categoría que tenga recursos).

Migraciones: `0001_initial` (tablas), `0002_align_id_fields` (ids `BigAutoField` de Django 6.1) y `0003_resource_resource_type` (nuevo campo opcional).

## Pruebas

```bash
python manage.py test pages
```

Ejecuta 59 pruebas con `TestCase`: 11 del Laboratorio 07, 18 del Laboratorio 08 y 30 del Laboratorio 09 (detalle, creación, edición y eliminación, validación del formulario, 404, 403/redirección por permisos y CSRF). Django crea y destruye la base separada `test_classroom_hub`; la base `classroom_hub` no se modifica.

## Qué no se versiona

`.venv/`, `.env`, credenciales, `db.sqlite3`, `__pycache__/` y `*.log`. Solo se publica `.env.example` con valores demostrativos. Los archivos de migración sí se versionan.

## Funcionalidades pendientes

CRUD público de categorías, búsqueda y filtros, carga de archivos, recuperación de contraseña, verificación de correo y API REST.
