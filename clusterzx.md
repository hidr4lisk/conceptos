````md
# Docker – Quick Start Flashcard (paperless-ai)

## 1. Descargar imagen
```bash
docker pull clusterzx/paperless-ai:latest
````

Descarga la imagen desde Docker Hub (plantilla, no se ejecuta).

---

## 2. Crear y ejecutar contenedor

```bash
docker run -d \
  --name paperless-ai \
  --network bridge \
  -v paperless-ai_data:/app/data \
  -p 3000:3000 \
  --restart unless-stopped \
  clusterzx/paperless-ai
```

### Flags clave

* `-d` → corre en segundo plano
* `--name` → nombre del contenedor
* `--network bridge` → red Docker por defecto
* `-v volumen:ruta` → persistencia de datos
* `-p host:contenedor` → exposición de puerto
* `--restart unless-stopped` → auto-restart

---

## 3. Ver contenedores activos

```bash
docker ps
```

---

## 4. Ver logs (debug)

```bash
docker logs paperless-ai
```

---

## 5. Acceder a la app

```text
http://localhost:3000
```

---

## 6. Control del contenedor

Parar:

```bash
docker stop paperless-ai
```

Arrancar:

```bash
docker start paperless-ai
```

Eliminar contenedor (datos persisten):

```bash
docker rm paperless-ai
```

---

## 7. Volúmenes

Listar volúmenes:

```bash
docker volume ls
```

Volumen usado:

```text
paperless-ai_data → /app/data
```

---

## 8. Regla mental Docker

* Imagen = plantilla
* Contenedor = proceso en ejecución
* Volumen = datos persistentes
* Borrar contenedor ≠ borrar datos

```
```
