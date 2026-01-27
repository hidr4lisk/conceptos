Perfecto. Voy a tratar esto como **tu primer proyecto real**, no como un TP. Paso a paso, orden lógico, sin asumir nada y sin saltos.

---

# 0. Idea clave antes de tocar código

**Primero funciona en local.
Después funciona en una VM.
Recién al final pensás en hosting.**

No empieces por “dónde lo subo”. Ese es un error clásico.

---

# 1. Preparar el entorno local (base sólida)

### 1.1 Sistema

* Ubuntu / Debian (lo que ya usás)
* Python 3.11
* PostgreSQL local

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip postgresql postgresql-contrib
```

---

### 1.2 Crear entorno virtual

```bash
mkdir corridor_dms
cd corridor_dms
python3 -m venv venv
source venv/bin/activate
```

---

### 1.3 Instalar dependencias

```bash
pip install django psycopg2-binary
```

(Después agregás más. Ahora solo lo mínimo.)

---

# 2. Crear el proyecto Django

```bash
django-admin startproject core
cd core
python manage.py startapp documents
```

Estructura mental:

```text
corridor_dms/
 ├─ venv/
 └─ core/
    ├─ core/
    ├─ documents/
    └─ manage.py
```

---

# 3. Base de datos (local primero)

### 3.1 Crear DB en PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE dms;
CREATE USER dms_user WITH PASSWORD 'dms_pass';
ALTER ROLE dms_user SET client_encoding TO 'utf8';
ALTER ROLE dms_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE dms_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE dms TO dms_user;
\q
```

---

### 3.2 Conectar Django a PostgreSQL

En `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dms',
        'USER': 'dms_user',
        'PASSWORD': 'dms_pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

# 4. Modelar los datos (el corazón del sistema)

En `documents/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User

class Corridor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DocumentType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Document(models.Model):
    filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    corridor = models.ForeignKey(Corridor, on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    sha256 = models.CharField(max_length=64)
    notes = models.TextField(blank=True)
```

---

### 4.1 Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

# 5. Usar el admin de Django (no reinventes nada)

En `documents/admin.py`:

```python
from django.contrib import admin
from .models import Corridor, DocumentType, Document

admin.site.register(Corridor)
admin.site.register(DocumentType)
admin.site.register(Document)
```

Probá:

```bash
python manage.py runserver
```

Entrá a:

```
http://127.0.0.1:8000/admin
```

Acá **ya podés cargar corredores y tipos** sin UI propia.

---

# 6. Login y permisos (simple y robusto)

Usá el auth nativo de Django.

En `settings.py`:

```python
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
```

Creá grupos:

* admin
* uploader
* viewer

Desde el admin.

---

# 7. Upload de archivos (parte crítica)

### 7.1 Directorio de archivos

```bash
mkdir /home/tu_usuario/dms_files
```

En `settings.py`:

```python
MEDIA_ROOT = '/home/tu_usuario/dms_files'
MEDIA_URL = '/media/'
```

---

### 7.2 Vista de upload (`documents/views.py`)

* Formulario HTML
* `request.FILES`
* Guardar archivo
* Calcular SHA256
* Crear objeto Document

Esto es el primer código “real” que escribís.
No lo apures. Acá se aprende.

---

# 8. Listado y búsqueda

* Vista con `QuerySet`
* Filtros por:

  * corredor
  * tipo
  * fecha
* Template simple con `<table>`

Nada de JS complejo.

---

# 9. Probar TODO en local

Checklist:

* login
* subir archivo
* ver listado
* descargar archivo
* revisar DB
* revisar filesystem

Hasta que esto no esté sólido, **no se mueve de local**.

---

# 10. Pasar a una máquina virtual (sandbox real)

### Opción simple

* VM local (VirtualBox / virt-manager)
* Ubuntu Server
* Clonar repo
* Repetir:

  * PostgreSQL
  * venv
  * migrate
  * runserver

Esto simula producción **sin riesgos**.

---

# 11. Recién acá pensás en hosting

Opciones cuando llegue el momento:

* VPS (DigitalOcean, Hetzner, etc.)
* Server institucional
* On-prem

La DB:

* **Siempre PostgreSQL**
* Nunca SQLite en prod

---

# 12. IA (olvidada por ahora, pero lista)

Mientras tanto:

* Guardá bien metadata
* No mezcles lógica
* Pensá el sistema como “fuente de verdad”

La IA se enchufa después, no ahora.

---

## Idea final (importante)

Este proyecto te enseña:

* arquitectura real
* disciplina
* despliegue
* errores reales

No es un curso.
Es tu **primer sistema serio**.

Si querés, el próximo paso natural es:

* escribir la **vista de upload paso a paso**
* o revisar estructura de carpetas para no romperla después
