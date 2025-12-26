CSRF (Cross-Site Request Forgery) es una vulnerabilidad web donde un atacante consigue que **el navegador de un usuario autenticado ejecute acciones no deseadas** en una aplicación web legítima.

El punto clave es este:
**el navegador envía automáticamente las cookies de sesión** al dominio objetivo. La aplicación confía en esas cookies y asume que la acción fue iniciada por el usuario legítimo, cuando en realidad fue forzada por el atacante.

No se roba la sesión.
Se **abusa de una sesión ya válida**.

---

## Ciclo de un ataque CSRF

Un CSRF funcional necesita tres condiciones simultáneas:

### 1. Conocimiento de la request

El atacante conoce:

* endpoint
* método (GET / POST)
* parámetros
* valores esperados

Ejemplo:

```
POST /transfer
amount=1000&to=attacker
```

### 2. Víctima autenticada + interacción

* El usuario está logueado en la aplicación objetivo
* El usuario interactúa con contenido controlado por el atacante

  * click
  * carga de imagen
  * auto-submit de formulario
  * ejecución de JS

El navegador adjunta automáticamente:

```
Cookie: session=abcdef123456
```

### 3. Falta de validación del lado servidor

La aplicación:

* no valida origen
* no usa token anti-CSRF
* no verifica intención del usuario

Resultado: la request forjada se ejecuta como legítima.

---

## Qué permite CSRF (impacto real)

CSRF **no filtra datos**, pero **modifica estado**.

Ejemplos típicos:

* cambio de contraseña
* cambio de email
* transferencia de dinero
* activación/desactivación de opciones
* acciones administrativas (si la víctima es admin)

---

## Por qué es peligroso

### Abuso de confianza

La aplicación confía en:

* cookies
* sesión activa
* navegador

Eso es insuficiente.

### Ejecución silenciosa

* No requiere malware
* No rompe SOP
* No genera alertas visibles
* El usuario suele no darse cuenta

### Escala

Un solo payload puede afectar a **todos los usuarios autenticados** que lo visiten.

---

## Resumen mental correcto

* CSRF ≠ robo de sesión
* CSRF = ejecución de acciones usando una sesión válida
* El navegador es el vector
* El fallo está en **no validar intención**

Es un problema de **lógica y control de confianza**, no de criptografía.


---

## CSRF tradicional (Traditional CSRF)

El CSRF tradicional se basa en **acciones que cambian estado** y se ejecutan mediante **envío de formularios** (HTML forms).

El ataque consiste en forzar al navegador de la víctima a enviar una request válida hacia una aplicación donde **ya está autenticada**, sin que la víctima sea consciente de ello.

Características clave:

* Uso de `<form>` HTML
* Métodos comunes: `POST` o `GET`
* El navegador adjunta automáticamente cookies de sesión
* No hay interacción visible más allá de un click o carga

### Flujo típico

1. La víctima está autenticada en su banco (cookie de sesión activa).
2. El atacante envía un link o email con contenido malicioso.
3. La víctima abre el link en el mismo navegador.
4. El contenido ejecuta un formulario auto-submit:

   ```
   POST /transfer
   amount=1000&to=attacker
   ```
5. El servidor procesa la request como legítima.

Resultado: transferencia, cambio de datos o acción crítica ejecutada.

---

## CSRF vía XMLHttpRequest / Fetch (CSRF asíncrono)

En aplicaciones modernas, muchas acciones no recargan la página. Se ejecutan mediante **AJAX** (`XMLHttpRequest` o `fetch`).

El vector cambia, pero el principio es idéntico:

* el navegador
* la cookie
* la falta de validación

### Diferencias con CSRF tradicional

* No hay `<form>`
* No hay recarga de página
* La acción se ejecuta vía JavaScript
* Endpoint suele ser `/api/*`

### Flujo de ataque

1. La víctima inicia sesión en `mailbox.thm`.
2. El atacante atrae a la víctima a una web maliciosa.
3. Esa web ejecuta JavaScript:

   ```js
   fetch("http://mailbox.thm/api/updateEmail", {
     method: "POST",
     body: "forward=attacker@mail.com"
   });
   ```
4. El navegador incluye:

   ```
   Cookie: session=xyz
   ```
5. El backend no valida CSRF y aplica el cambio.

Resultado: modificación silenciosa de preferencias.

Nota:

* SOP no bloquea el envío de la request
* SOP solo bloquea la **lectura** de la respuesta

---

## CSRF basado en Flash (Flash-based CSRF)

Flash-based CSRF explotaba debilidades en **Adobe Flash Player**, permitiendo que archivos `.swf` enviaran requests arbitrarias a otros dominios.

### Funcionamiento

* El atacante alojaba un archivo `.swf` malicioso
* El archivo ejecutaba requests HTTP a sitios donde la víctima estaba autenticada
* El navegador adjuntaba cookies automáticamente
* El servidor aceptaba la acción

Esto era especialmente peligroso porque:

* Flash tenía su propio stack de red
* Muchas aplicaciones confiaban en `crossdomain.xml`
* Las defensas CSRF eran inexistentes o débiles

### Estado actual

* Flash dejó de ser soportado el **31/12/2020**
* No es relevante para aplicaciones modernas
* Sigue siendo **importante para sistemas legacy**

---

## Resumen comparativo

| Tipo de CSRF | Vector    | Tecnología             |
| ------------ | --------- | ---------------------- |
| Tradicional  | HTML form | POST / GET             |
| Asíncrono    | JS        | XMLHttpRequest / Fetch |
| Flash-based  | SWF       | Flash network stack    |

En todos los casos:

* el navegador es el intermediario
* la sesión es válida
* el fallo está en no validar intención

CSRF siempre es un problema de **confianza mal definida**, no de autenticación.
