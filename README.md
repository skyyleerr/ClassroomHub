# ClassroomHub

Portal web de recursos de aprendizaje construido con Django (programa ADSO, laboratorios de Python). El Laboratorio 06 creó las tres páginas con plantillas compartidas; el Laboratorio 07 sustituye la lista de recursos escrita en `views.py` por un catálogo **persistente en MySQL o MariaDB**, administrable desde Django Admin.

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

El superusuario es una cuenta de Django, distinta del usuario SQL. Abre http://127.0.0.1:8000/admin/, crea categorías y recursos, y revisa http://127.0.0.1:8000/resources/.

## Rutas

| Ruta | Nombre | Descripción |
|---|---|---|
| `/` | `pages:home` | Página principal |
| `/resources/` | `pages:resources` | Recursos consultados con el ORM (título, descripción, categoría y disponibilidad); muestra un mensaje si el catálogo está vacío |
| `/resources/available/` | `pages:available_resources` | Solo recursos disponibles (reto adicional, solo lectura) |
| `/about/` | `pages:about` | Propósito del proyecto |
| `/admin/` | — | Django Admin (categorías y recursos) |

Cualquier otra dirección responde `404`.

## Modelos

- `Category`: `name` (único), `description`.
- `Resource`: `title`, `description`, `available`, `resource_type`, `created_at` y `category` (`ForeignKey` con `related_name="resources"` y `on_delete=PROTECT`, por lo que no se puede borrar una categoría que tenga recursos).

Migraciones: `0001_initial` (tablas), `0002_align_id_fields` (ids `BigAutoField` de Django 6.1) y `0003_resource_resource_type` (nuevo campo opcional).

## Pruebas

```bash
python manage.py test pages
```

Ejecuta 11 pruebas con `TestCase`: las diez del laboratorio (páginas, navegación, 404, categoría relacionada, persistencia, protección de borrado, catálogo vacío y relación inversa) más la de `/resources/available/`. Django crea y destruye la base separada `test_classroom_hub`; la base `classroom_hub` no se modifica.

## Qué no se versiona

`.venv/`, `.env`, `db.sqlite3`, `__pycache__/` y `*.log`. Solo se publica `.env.example` con valores demostrativos. Los archivos de migración sí se versionan.

## Funcionalidades pendientes

Registro público de usuarios, autenticación propia, formularios públicos, CRUD desde vistas personalizadas y API REST. El siguiente laboratorio incorpora autenticación, sesiones, grupos y permisos.
