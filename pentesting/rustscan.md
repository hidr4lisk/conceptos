Aquí está la flashcard completa, centrada **solo en RustScan con Docker (Moby)** en Parrot OS, lista para reproducir. Incluye instalación, razones y un ejemplo funcional.

---

## **Flashcard: RustScan en Parrot OS (Docker/Moby)**

### 1️⃣ Instalar Rust & Cargo

**Por qué:** RustScan está escrito en Rust; Cargo es el gestor de paquetes y compilador de Rust. Necesario si alguna vez compilas desde fuente o quieres usar herramientas Rust relacionadas.

**Comandos:**

```bash
# Instala rustup (Rust + Cargo)
curl https://sh.rustup.rs -sSf | sh

# Reinicia shell o ejecuta
source $HOME/.cargo/env

# Verificar instalación
rustc --version
cargo --version
```

---

### 2️⃣ Instalar Docker en Parrot OS usando Moby

**Por qué Moby:** Parrot no tiene release compatible con Docker CE. `moby-engine` y `moby-cli` funcionan igual, mantienen compatibilidad total con Docker y evitan errores de repositorio (`lory`).

**Comandos:**

```bash
# Eliminar repositorio Docker inválido
sudo rm /etc/apt/sources.list.d/docker.list
sudo apt update

# Instalar motor y CLI de Docker (Moby)
sudo apt install -y moby-engine moby-cli moby-buildx

# Instalar docker-compose (opcional)
sudo apt install -y docker-compose

# Habilitar servicio
sudo systemctl enable --now moby

# Probar instalación
docker --version
docker run hello-world

# Ejecutar docker sin sudo (opcional)
sudo usermod -aG docker $USER
newgrp docker
```

---

### 3️⃣ RustScan con Docker

**Por qué:**

* Evita instalar Nmap, Rust o Cargo localmente.
* Evita problemas de límites de archivos abiertos (`ulimit`).
* Asegura siempre versión estable de RustScan.

**Comando reproducible (Linux, host network):**

```bash
docker run -it --rm --network host rustscan/rustscan:2.1.1 192.168.1.0/24 -t 500 -b 1500 -- -A
```

**Alias recomendado:**

```bash
alias rustscan='docker run -it --rm --network host rustscan/rustscan:2.1.1'
# Uso luego:
rustscan 192.168.1.0/24 -t 500 -b 1500 -- -A
```

---

### 4️⃣ Conceptos clave

* **Docker/Moby:** contenedor = proceso aislado con librerías y dependencias propias, portable entre sistemas.
* **`--network host`:** el contenedor ve la red del host (Linux).
* **Flags `-t` y `-b`:** controlan threads y batch size; necesarios para rendimiento sin sobrecargar el sistema.

---

### 5️⃣ Ejemplo de uso

Escanear toda la red local, detectar servicios y versiones con Nmap integrado:

```bash
rustscan 192.168.1.0/24 -t 500 -b 1500 -- -A
```

---
