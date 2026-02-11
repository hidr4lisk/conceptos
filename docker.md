Perfecto. Vamos paso a paso, asumiendo **cero experiencia previa con Docker** y sin saltos conceptuales.

---

## 1. Qué es Docker (en una frase)

Docker ejecuta aplicaciones dentro de **contenedores**: entornos aislados que ya traen todo lo necesario para funcionar (dependencias, runtime, configuración básica).

No instala la app “en tu sistema”, la encapsula.

---

## 2. Qué hace exactamente lo que te pasaron

### Paso 1

```bash
docker pull clusterzx/paperless-ai:latest
```

**Qué hace**

* Descarga una *imagen* desde Docker Hub.
* `clusterzx/paperless-ai` = nombre del proyecto.
* `latest` = versión más reciente.

Una **imagen** es una plantilla inmutable. No se ejecuta todavía.

---

### Paso 2

```bash
docker run -d \
    --name paperless-ai \
    --network bridge \
    -v paperless-ai_data:/app/data \
    -p 3000:3000 \
    --restart unless-stopped \
    clusterzx/paperless-ai
```

Esto **crea y ejecuta un contenedor** a partir de la imagen.

Vamos flag por flag:

---

## 3. Desglose técnico del `docker run`

### `docker run`

* Crea un contenedor nuevo
* Lo inicia inmediatamente

---

### `-d`

* *Detached mode*
* Corre en segundo plano (no ocupa la terminal)

---

### `--name paperless-ai`

* Nombre legible del contenedor
* Útil para `docker stop`, `docker logs`, `docker exec`

---

### `--network bridge`

* Usa la red por defecto de Docker
* Permite exponer puertos al host
* Correcto para uso local

---

### `-v paperless-ai_data:/app/data`

* **Persistencia de datos**
* `paperless-ai_data` = volumen Docker (vive fuera del contenedor)
* `/app/data` = ruta interna donde la app guarda info

Sin esto, al borrar el contenedor **perdés todo**.

---

### `-p 3000:3000`

* Mapeo de puertos
* `host:contenedor`

Resultado:

* Accedés desde tu navegador a:

  ```
  http://localhost:3000
  ```

---

### `--restart unless-stopped`

* El contenedor se reinicia solo:

  * al reboot
  * si crashea
* **No** se reinicia si lo parás manualmente

---

### `clusterzx/paperless-ai`

* Imagen base usada para crear el contenedor

---

## 4. Qué deberías ver después

### Ver contenedores corriendo

```bash
docker ps
```

Debería aparecer algo como:

```
paperless-ai   clusterzx/paperless-ai   Up ...
```

---

### Ver logs (muy importante la primera vez)

```bash
docker logs paperless-ai
```

Si hay errores, aparecen ahí.

---

### Acceso a la app

Abrís el navegador:

```
http://localhost:3000
```

---

## 5. Comandos mínimos de supervivencia Docker

Parar el contenedor:

```bash
docker stop paperless-ai
```

Arrancarlo de nuevo:

```bash
docker start paperless-ai
```

Borrarlo (no borra el volumen):

```bash
docker rm paperless-ai
```

Ver volúmenes:

```bash
docker volume ls
```

---

## 6. Qué **NO** hace esto (importante)

* No toca Python del sistema
* No instala paquetes globales
* No modifica tu Ubuntu
* No expone nada a Internet (solo localhost)

---

## 7. Riesgos reales

* El riesgo principal es **confiar en la imagen**
* Estás ejecutando código de un tercero con permisos de contenedor
* Para entorno local/lab está bien
* Para producción: revisar Dockerfile, tags versionados, no `latest`

---

Si el contenedor **no levanta**, el siguiente paso lógico es:

```bash
docker logs paperless-ai
```

Ahí se depura todo.
