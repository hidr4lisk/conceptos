**Resumen técnico – HTTP/2 y Request Smuggling**

### Cambios clave de HTTP/2

HTTP/2 rediseña el protocolo para eliminar limitaciones de HTTP/1.1.

* **Protocolo binario**:
  No es human-readable. Facilita parsing determinístico y reduce errores.
* **Comunicación estructurada**:
  Cliente y servidor intercambian frames binarios con tamaños explícitos.

---

### Estructura de una request HTTP/2

1. **Pseudo-headers** (obligatorios, prefijo `:`):

   * `:method`
   * `:path`
   * `:scheme`
   * `:authority`

2. **Headers normales**

   * Todos en **lowercase**.
   * Ej: `user-agent`, `content-length`.

3. **Request Body**

   * Datos POST, archivos, payloads, etc.

---

### Diferencia estructural crítica vs HTTP/1.1

HTTP/2 **no depende de separadores textuales** (`\r\n`, `:`):

* Cada componente está **prefijado con su tamaño**.
* El parser sabe exactamente:

  * Dónde empieza.
  * Cuánto mide.
  * Dónde termina cada campo.

Ejemplo:

* Header name → longitud explícita.
* Header value → longitud explícita.
* Body → longitud explícita.

---

### Impacto en Request Smuggling

En HTTP/1.1:

* Existen múltiples formas de definir el tamaño del body (`Content-Length`, `Transfer-Encoding`).
* Diferentes servidores interpretan distinto → smuggling.

En HTTP/2:

* **No hay ambigüedad de límites**.
* `Content-Length` y `Transfer-Encoding` **no controlan el parsing**.
* El tamaño real está definido a nivel de frame.

Resultado:

* **Request smuggling es prácticamente imposible en HTTP/2 puro**.

---

### Detalle importante

Aunque HTTP/2 no usa `Content-Length` para parsing:

* Los navegadores **siguen enviándolo**.
* Motivo: **downgrade HTTP/2 → HTTP/1.1** en proxies o back-ends legacy.

Esto es crítico en escenarios mixtos.

---

### Superficie real de ataque

El smuggling **no ocurre dentro de HTTP/2**, sino en:

* **Load balancers / reverse proxies HTTP/2**
* **Back-ends HTTP/1.1**

Flujo típico vulnerable:

```
Client (HTTP/2)
   ↓
Proxy / LB (HTTP/2)
   ↓ downgrade
Back-end (HTTP/1.1)
```

Si el downgrade no es consistente:

* Reaparecen ambigüedades de HTTP/1.1.
* Vuelven CL.TE, TE.CL y TE.TE.

---

### Idea clave

**HTTP/2 elimina el request smuggling a nivel de protocolo**,
pero **las arquitecturas híbridas HTTP/2 ↔ HTTP/1.1 reintroducen el problema**.
El riesgo está en el **downgrade y la traducción entre protocolos**, no en HTTP/2 en sí.


**Resumen técnico – HTTP/2 Downgrading y Request Smuggling**

---

### Qué es HTTP/2 Downgrading

Ocurre cuando:

* **Frontend** (cliente ↔ proxy) usa **HTTP/2**.
* **Backend** (proxy ↔ servidor) usa **HTTP/1.1**.

El proxy traduce requests HTTP/2 a HTTP/1.1.
Esta conversión **reintroduce ambigüedades de HTTP/1.1**, habilitando **HTTP desync / request smuggling**.

El ataque **no rompe HTTP/2**, rompe la **traducción HTTP/2 → HTTP/1.1**.

---

### Idea central del ataque

El atacante:

* Envía **HTTP/2 requests** cuidadosamente manipuladas.
* El proxy las convierte en **HTTP/1.1 inválidas o ambiguas**.
* El backend entra en **estado desincronizado**.
* Requests de otros usuarios quedan contaminadas.

---

### Comportamiento esperado (ideal)

Un proxy debería:

* Convertir **1 request HTTP/2 → 1 request HTTP/1.1**.
* Ajustar correctamente límites y headers.

En la práctica:

* Cada proxy implementa la conversión distinto.
* Algunos **copian headers peligrosos sin validación**.

---

## Técnicas principales en HTTP/2 Downgrading

---

### H2.CL (HTTP/2 → Content-Length)

**Concepto**

* HTTP/2 **no usa** `Content-Length`.
* El atacante **inyecta `Content-Length` en HTTP/2**.
* El proxy lo pasa intacto al backend HTTP/1.1.

**Efecto**

* Backend confía en `Content-Length`.
* Ejemplo: `Content-Length: 0`

  * Backend cree que no hay body.
  * El body real queda en el buffer → **request smuggling**.

**Resultado**

* Backend queda esperando más datos.
* El siguiente request (de otra víctima) se concatena.

---

### H2.TE (HTTP/2 → Transfer-Encoding)

**Concepto**

* El atacante inyecta `Transfer-Encoding: chunked` en HTTP/2.
* El proxy lo reenvía al backend HTTP/1.1.

**Efecto**

* Backend procesa body como chunked.
* Primer chunk `0` → body finalizado.
* El resto del body HTTP/2 **envenena la conexión**.

**Resultado**

* Mismo impacto que H2.CL:

  * Desync.
  * Requests de víctimas alteradas.

---

### CRLF Injection en HTTP/2

**Fundamento**

* HTTP/2 permite **datos binarios arbitrarios**.
* Se puede inyectar `\r\n` en headers o valores.

**Durante el downgrade**

* El proxy traduce esos bytes a HTTP/1.1.
* `\r\n` se interpreta como:

  * Separador de headers.
  * Fin de headers.
  * Inicio de un nuevo request.

**Capacidades**

* Inyección de headers.
* Smuggling de requests completos.
* No limitado solo a headers: cualquier campo vulnerable.

**Limitación**

* Depende fuertemente del proxy y su sanitización.

---

## Ejemplo práctico (H2.CL con backend compartido)

Escenario:

* Proxy HTTP/2 (Varnish antiguo).
* **Una sola conexión backend compartida** entre usuarios.

Ataque:

1. Enviar HTTP/2 POST con `Content-Length: 0`.
2. Smugglear un GET incompleto:

   ```
   GET /post/like/<id>
   X: f
   ```
3. El backend espera completar la request.
4. El siguiente usuario conecta.
5. Su request se concatena.
6. Backend procesa:

   * Like al post del atacante.
   * Con cookies de la víctima.

Resultado:

* **Acción ejecutada como otro usuario**.
* Sin interacción visible de la víctima.

---

### Detalles operativos críticos

* No enviar requests propios tras envenenar la conexión.
* No dejar `\r\n` extra (rompe concatenación).
* En Burp:

  * Confirmar HTTP/2.
  * Desactivar *Update Content-Length*.
  * Controlar timing (esperar requests de víctimas).

---

### Idea clave

**HTTP/2 es seguro por diseño**,
pero **HTTP/2 → HTTP/1.1 downgrading rompe esa seguridad**.

El ataque vive en:

* Proxies.
* Load balancers.
* Traducciones imperfectas.

**El objetivo no es HTTP/2, sino la frontera entre protocolos.**



### Request Tunneling vs Desync (HTTP Request Smuggling)

#### 1. Diferencia estructural

**Request Desync (clásico)**

* El frontend (proxy) y el backend **comparten una conexión persistente**.
* Un atacante **desincroniza** ambos parsers (CL/TE, TE/CL, etc.).
* El payload inyectado **impacta requests de otros usuarios**.
* Efectos típicos: session hijacking, cache poisoning cross-user.

**Request Tunneling**

* El frontend asigna **una conexión backend por usuario**.
* No hay mezcla de tráfico entre usuarios.
* El atacante **solo afecta su propia conexión**.
* Aun así, puede **inyectar múltiples requests ocultas** dentro de una request válida.
* Impacto: bypass de controles del frontend, acceso a endpoints internos, lógica inesperada en backend.

Resumen rápido:

```
Desync  -> cross-user impact (shared backend connection)
Tunneling -> single-user impact (per-user backend connection)
```

---

#### 2. Qué cambia cuando hay per-user backend connections

* El proxy **aísla conexiones** para evitar contaminación entre usuarios.
* Se elimina el vector “envenenar al siguiente usuario”.
* Pero **no se elimina el bug de parsing** entre frontend y backend.
* Si el frontend acepta una request “mal formada” y el backend la interpreta distinto → **smuggling local**.

Eso es **request tunneling**:

> “Smuggleás requests, pero viajan solo por tu túnel”.

---

#### 3. Por qué sigue siendo explotable

Aunque no puedas afectar a otros usuarios, todavía podés:

* Bypassear ACLs del frontend
* Saltar autenticación frontend-only
* Acceder a endpoints internos (`/admin`, `/internal`, `/debug`)
* Ejecutar requests que el frontend bloquearía por método/path
* Encadenar requests (pipeline oculto)

Ejemplo conceptual:

```
[Request visible al proxy]
POST /public HTTP/1.1
Content-Length: X

[Request oculta para backend]
GET /admin HTTP/1.1
Host: backend
```

El proxy ve **una** request válida.
El backend procesa **dos**.

---

#### 4. Caso del lab: HAProxy vulnerable (CVE-2019-19330)

Datos clave:

* **Frontend:** HAProxy viejo
* **Vulnerabilidad:** CRLF injection
* **Backend:** app vulnerable
* **Acceso:** `https://10.65.187.207:8100`

Qué permite CVE-2019-19330:

* Inyectar `\r\n` en headers
* Terminar headers prematuramente
* Forzar al backend a parsear **requests adicionales**

Esto **no requiere** conexiones compartidas.
Funciona perfectamente con **per-user backend connections**.

---

#### 5. Modelo mental correcto

```
Frontend (HAProxy)
- Cree que envió 1 request
- Aplica reglas solo a esa

Backend
- Recibe N requests
- Ejecuta todas
```

No hay “desync entre usuarios”, pero sí:

* **Desync entre capas**
* **Túnel de requests encadenadas**

---

#### 6. Conclusión operativa

* **Desync** es más potente, pero depende de conexiones compartidas.
* **Tunneling** es más común en arquitecturas modernas.
* Impacto menor, pero **suficiente para bypass críticos**.
* En este lab: el objetivo es **inyectar requests ocultas usando CRLF** y observar cómo el backend las ejecuta aunque el frontend no las vea.

Idea clave:

> *Per-user backend connection no elimina request smuggling; solo lo confina.*



Voy a **desarmarlo en flujo técnico**, sin narrativa.

---

## Objetivo

**Filtrar headers internos que el frontend (HAProxy) agrega antes de enviar la request al backend**, usando **request tunneling + CRLF injection**.

No desync cross-user.
Todo ocurre **en tu propio backend connection**.

---

## Arquitectura relevante

```
Browser (HTTP/2)
   ↓
HAProxy (vulnerable, downgrade HTTP/2 → HTTP/1.1)
   ↓
Backend app (HTTP/1.1)
```

Puntos clave:

* El browser envía **HTTP/2**
* HAProxy convierte a **HTTP/1.1**
* HAProxy **inyecta headers internos** (Host, X-Internal-*, etc.)
* HAProxy es vulnerable a **CRLF injection en headers** (CVE-2019-19330)

---

## Por qué se puede filtrar info

El backend:

* Tiene un endpoint `/hello`
* Refleja el parámetro `q` del body en la response

Si logramos que:

* Los **headers internos** terminen dentro del **body del backend**
  → el backend **nos los devuelve reflejados**

---

## Idea central del ataque

1. Enviar **1 request HTTP/2**
2. HAProxy la transforma en **2 requests HTTP/1.1**
3. La **segunda request** contiene en su body:

   * headers internos agregados por HAProxy
4. El backend los refleja vía `q=...`

Eso es **request tunneling**.

---

## Mecánica exacta

### Paso 1 — Request base (HTTP/2)

```http
POST /hello HTTP/2
Host: 10.65.187.207:8100
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
```

Notas:

* `Content-Length` **existe aunque HTTP/2 lo ignore**
* Es crítico porque el backend sí lo usa tras el downgrade

---

### Paso 2 — Header inyectable (CRLF)

Se agrega un header controlado:

```
Foo: <payload>
```

Ese payload incluye:

* `\r\n` para cerrar headers
* `Content-Length: 0` para **forzar fin del body**
* Una **segunda request completa**

---

### Paso 3 — Payload conceptual (lo que ve el backend)

```http
POST /hello HTTP/1.1
Host: 10.65.187.207
Content-Length: 0

POST /hello HTTP/1.1
Host: 10.65.187.207
Content-Type: application/x-www-form-urlencoded
Content-Length: 300

q=<AQUÍ CAEN LOS HEADERS INTERNOS>
```

Cómo llegan ahí:

* HAProxy agrega headers **después** de los del cliente
* Esos headers quedan **entre** las dos requests
* El backend los interpreta como parte del body de la segunda

---

## Por qué hay que inyectar `Host`

HTTP/1.1 **requiere Host** por request.

La primera request:

* Termina antes de que HAProxy agregue su `Host`
* Si no inyectás uno → backend rechaza la request

Por eso el payload **incluye un Host explícito**.

---

## Content-Length del segundo POST

```http
Content-Length: 300
```

Función:

* Reservar espacio suficiente para que entren:

  * Host agregado por proxy
  * X-Internal-*
  * otros headers

Valores:

* Muy chico → headers truncados
* Muy grande → backend queda esperando bytes → conexión colgada

Es **trial & error**.

---

## Ejecución en Burp (clave técnica)

* Repeater debe ser **HTTP/2**
* `Update Content-Length` → **OFF**
* El payload **NO se edita en texto**
* Se edita en **Inspector**
* CRLF = `SHIFT + ENTER`
* Al aplicar → request queda **kettled**

“Kettled” = no representable como texto plano.

---

## Por qué hay que enviar la request dos veces

* Primera vez:

  * Se procesa la **primera request**
  * Response vacía
* Segunda vez:

  * El backend ya tiene la conexión
  * Procesa la **segunda request**
  * Refleja `q=...` → headers internos visibles

---

## Resultado esperado

Response contiene algo como:

```
Host: backend
X-Internal-User: proxy
X-Forwarded-For: 10.x.x.x
...
```

Eso confirma:

* Request tunneling exitoso
* Headers internos filtrados
* Parsing inconsistente frontend/backend

---

## Resumen mental (en una línea)

> **CRLF en HTTP/2 header → downgrade mal parseado → headers internos caen en body → backend los refleja**

Eso es **Leaking Internal Headers vía Request Tunneling**.
