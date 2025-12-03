Explicación de ese comando:

* * *

### Comando

```bash
find / -type f -perm -04000 -ls 2>/dev/null
```

* * *

### Desglose

- `find /` → busca desde la raíz del sistema.
    
- `-type f` → solo archivos normales (no directorios, sockets, etc).
    
- `-perm -04000` → filtra archivos con el bit **SUID** activo.
    
    - **SUID** = *Set User ID*: si un archivo binario lo tiene, cuando lo ejecuta cualquier usuario, se ejecuta con los privilegios del **dueño** (ej. root).
    - Para SGID se usaría `-02000`.
- `-ls` → lista los resultados con permisos, propietario, etc (similar a `ls -l`).
    
- `2>/dev/null` → descarta errores de “Permission denied” para no ensuciar la salida.
    

* * *

### Ejemplo de salida

```
123456   120 -rwsr-xr-x   1 root   root   114K Apr  7  2020 /usr/bin/passwd
```

Aquí:

- `-rwsr-xr-x` → la `s` en lugar de `x` en la parte de usuario (`rws`) indica **SUID**.
- Propietario = root.
- Archivo = `/usr/bin/passwd`.

* * *

### Relevancia en pentesting

- Binarios con SUID root pueden usarse para escalar privilegios.
- Ejemplo: si `find` o `vim` están con SUID root, puedes usarlos para ejecutar comandos como root (exploits documentados en GTFOBins).

* * *

¿Quieres que te arme una **tabla de binarios SUID más comunes + cómo explotarlos** (passwd, find, vim, nmap, etc)?