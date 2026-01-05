**Resumen técnico – HTTP Request Structure y Request Smuggling**

Una **HTTP request** se compone de **headers** y **body**, con una estructura estricta que define cómo el servidor interpreta el mensaje.

### Estructura de una HTTP Request

1. **Request Line**
   Formato:
   `METHOD /path HTTP/version`

   * **Method**: acción (GET, POST, etc.).
   * **Path**: recurso objetivo.
   * **HTTP version**: especificación usada (HTTP/1.1 vs HTTP/2 difieren en parsing).

2. **Request Headers**
   Metadatos que controlan el procesamiento del request: tipo de contenido, autenticación, caché, parsing del body, etc.

3. **Message Body**
   Contenido real del request.

   * Puede estar vacío (GET).
   * En POST/PUT suele contener form data, JSON, archivos.

### Headers críticos para el parsing

#### Content-Length

* Indica el **tamaño exacto del body en bytes**.
* El servidor lee exactamente esa cantidad de datos.
* Ejemplo:
  `Content-Length: 14` → el body tiene 14 bytes.

#### Transfer-Encoding

* Define **cómo** se transmite el body.
* `chunked`: el body se divide en chunks.

  * Cada chunk empieza con su tamaño en **hexadecimal**.
  * Finaliza con un chunk de tamaño `0`.

Ejemplo conceptual:

```
b        -> tamaño del chunk (hex)
data     -> contenido
0        -> fin del body
```

### Impacto de los headers en el procesamiento

* Determinan **dónde empieza y termina** una request.
* Influyen en autenticación, caché, redirecciones y parsing del body.
* Un parsing inconsistente rompe el modelo de request/response.

### Origen del HTTP Request Smuggling

El **HTTP Request Smuggling** ocurre cuando **dos componentes interpretan distinto los límites del request**, típicamente:

* **Front-end** (proxy, load balancer).
* **Back-end** (application server).

Casos comunes:

* Presencia simultánea de `Content-Length` y `Transfer-Encoding`.
* Un componente prioriza `Content-Length`, el otro `Transfer-Encoding`.

### Consecuencia

* El front-end cree que el request termina en un punto.
* El back-end cree que continúa.
* Parte del tráfico queda **“smuggled”** dentro de otra request.

Resultado:

* Requests ocultos.
* Bypass de controles de seguridad.
* Desincronización del flujo HTTP.
* Impacto potencial: cache poisoning, auth bypass, request injection.

### Idea clave

**HTTP Request Smuggling no es un bug aislado**, es una **desincronización de parsing HTTP** causada por interpretaciones inconsistentes de headers críticos entre servidores encadenados.



**Resumen técnico – HTTP Request Smuggling CL.TE**

### Qué es CL.TE

**CL.TE (Content-Length / Transfer-Encoding)** es una técnica de HTTP Request Smuggling basada en una **priorización distinta de headers** entre componentes:

* **Front-end (proxy / load balancer)** → usa `Content-Length`.
* **Back-end (application server)** → usa `Transfer-Encoding`.

La ambigüedad aparece cuando **ambos headers están presentes** en la misma request.

---

### Mecanismo de funcionamiento

1. El atacante envía una request con:

   * `Content-Length`
   * `Transfer-Encoding: chunked`

2. **Front-end**:

   * Confía en `Content-Length`.
   * Cree que el request termina cuando se consumen esos bytes.

3. **Back-end**:

   * Confía en `Transfer-Encoding`.
   * Interpreta los chunks y considera `0` como fin del body.

Resultado:

* El front-end cree que todo es **una sola request**.
* El back-end interpreta que hay **otra request adicional** embebida.

Esto genera **desincronización HTTP**.

---

### Ejemplo conceptual de explotación

* El `0` indica fin del body chunked para el back-end.
* Todo lo que sigue es tratado como **una nueva request**.
* El back-end puede procesar un `POST /update` no previsto por el front-end.

Impacto típico:

* Ejecución de requests no autorizadas.
* Bypass de autenticación.
* Manipulación de estado (ej. `isadmin=true`).

---

### Rol crítico del Content-Length

Para que el smuggling funcione:

* El `Content-Length` **debe estar calculado con precisión** respecto al punto donde el front-end deja de leer.
* Si el valor es incorrecto:

  * El back-end puede leer solo parte del body.
  * El payload smuggled puede quedar truncado o ignorado.

Ejemplo:

* Body real: `username=test&query=test` → **24 bytes**
* `Content-Length: 10`

  * El back-end solo procesa los primeros 10 bytes.
  * El resto queda fuera del parsing esperado.

Consecuencia:

* Datos incompletos.
* Smuggling fallido o comportamiento inesperado.

---

### Idea clave

**CL.TE explota un desacople de parsing HTTP**:

* Un componente define el final del request por tamaño fijo.
* Otro lo define por chunks.
* El atacante controla esa discrepancia para inyectar requests ocultas.

No es un error de aplicación, sino un **fallo de diseño en la cadena HTTP front-end ↔ back-end**.


**Resumen técnico – HTTP Request Smuggling TE.CL**

### Qué es TE.CL

**TE.CL (Transfer-Encoding / Content-Length)** es la variante inversa de CL.TE.

Prioridades:

* **Front-end / proxy** → prioriza `Transfer-Encoding`.
* **Back-end / application server** → prioriza `Content-Length`.

La vulnerabilidad aparece cuando **ambos headers coexisten** y cada componente usa uno distinto para definir el fin del request.

---

### Mecanismo de funcionamiento

1. El atacante envía una request con:

   * `Transfer-Encoding: chunked`
   * `Content-Length` bajo o inconsistente.

2. **Front-end**:

   * Parsea el body como `chunked`.
   * Considera todo hasta el chunk `0` como **un solo request**.

3. **Back-end**:

   * Ignora `Transfer-Encoding`.
   * Lee solo los **N bytes indicados por `Content-Length`**.

Resultado:

* El back-end termina el request antes que el front-end.
* El resto del tráfico queda **pendiente en el buffer** y se procesa como **una nueva request**.

---

### Ejemplo conceptual de explotación

* El front-end interpreta `78` (hex) como tamaño del chunk y absorbe todo el contenido hasta `0`.
* El back-end solo consume `Content-Length: 4`.
* Todo lo que sigue (`POST /update ...`) se interpreta como **request independiente**.

Efecto:

* Ejecución de requests no previstas.
* Alteración de estado (`isadmin=true`).
* Bypass de controles de acceso si el endpoint lo permite.

---

### Diferencia clave con CL.TE

| Técnica | Front-end usa     | Back-end usa      |
| ------- | ----------------- | ----------------- |
| CL.TE   | Content-Length    | Transfer-Encoding |
| TE.CL   | Transfer-Encoding | Content-Length    |

En **TE.CL**, el front-end espera más datos de los que el back-end procesa.

---

### Impacto

* Request injection persistente.
* Privilege escalation.
* Cache poisoning.
* Desincronización del pipeline HTTP.

---

### Idea clave

**TE.CL explota un cierre anticipado del request en el back-end** causado por `Content-Length`, mientras el front-end sigue tratando el tráfico como parte del body `chunked`.
El atacante controla el desfase y fuerza la ejecución de requests ocultas.


**Resumen técnico – HTTP Request Smuggling TE.TE**

### Qué es TE.TE

**TE.TE (Transfer-Encoding / Transfer-Encoding)** es una técnica de request smuggling donde **tanto el front-end como el back-end usan `Transfer-Encoding`**, pero **lo interpretan de forma distinta**.

A diferencia de CL.TE y TE.CL:

* No depende necesariamente de `Content-Length`.
* Se basa en **Transfer-Encoding malformado u obfuscado**.

---

### Origen de la vulnerabilidad

El problema surge cuando:

* El header `Transfer-Encoding` contiene valores **no estándar** o múltiples entradas.
* Cada componente HTTP **normaliza, filtra o prioriza** esos valores de manera distinta.

Ejemplos comunes:

* `Transfer-Encoding: chunked`
* `Transfer-Encoding: chunked1`
* Espacios, mayúsculas, separadores inválidos, múltiples headers TE.

---

### Mecanismo de funcionamiento

1. El atacante envía una request con:

   * `Transfer-Encoding` válido.
   * `Transfer-Encoding` malformado u obfuscado.
   * `Content-Length` de apoyo.

2. **Front-end**:

   * Ignora o descarta el TE malformado.
   * Usa `Transfer-Encoding: chunked`.
   * Parsea todo hasta el chunk `0` como **un solo request**.

3. **Back-end**:

   * Interpreta distinto el TE malformado.
   * Puede:

     * Ignorar TE y caer en `Content-Length`.
     * Parsea el body de forma inconsistente.

Resultado:

* Desincronización de límites del request.
* Aparición efectiva de **CL.TE o TE.CL inducido**.

---

### Ejemplo conceptual de explotación

* Front-end: trata el body como `chunked` completo.
* Back-end: solo consume `Content-Length: 4`.
* El payload `POST /update` queda **desacoplado** y se ejecuta como request independiente.

---

### Relación con otras técnicas

TE.TE **no es un tercer parsing estable**, sino un **disparador**:

* Si el front-end ignora TE → CL.TE.
* Si el back-end ignora TE → TE.CL.

El atacante **fuerza el fallback** explotando diferencias de parsing.

---

### Impacto

* Request injection persistente.
* Privilege escalation (`isadmin=true`).
* Bypass de autenticación.
* Cache poisoning.
* Corrupción del flujo HTTP.

---

### Idea clave

**TE.TE explota inconsistencias en la normalización del header `Transfer-Encoding`**.
Mediante obfuscación, induce a los servidores a **usar reglas distintas**, creando una desincronización que permite smuggling sin depender directamente de `Content-Length`.
