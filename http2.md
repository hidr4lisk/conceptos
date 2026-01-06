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
