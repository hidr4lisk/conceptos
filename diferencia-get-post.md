En un entorno web la diferencia es estructural y afecta cómo explotas, interceptás y manipulas tráfico en un laboratorio.

GET
Transporta parámetros en la URL.
Impacto:

1. Visibles en logs, historial y referers.
2. Longitud limitada.
3. Se usan para operaciones idempotentes: lectura, navegación, enumeración.
4. Vectores típicos: XSS reflejado, SQLi de enumeración, LFI/RFI, fuzzing de parámetros, manipulación directa desde el navegador.

Sintaxis base:
`GET /search.php?q=test HTTP/1.1`
`Host: target`

En Burp o ZAP: modificación inmediata en la línea de petición.

POST
Transporta parámetros en el body.
Impacto:

1. No visibles en la URL.
2. Permite contenidos grandes: JSON, formularios, binarios.
3. Se usa para operaciones no idempotentes: login, creación, actualización.
4. Vectores típicos: bruteforce de credenciales, bypass de validaciones del lado del cliente, manipulación de payloads JSON/XML, CSRF, ataques a lógica.

Sintaxis base:
`POST /login HTTP/1.1`
`Host: target`
`Content-Type: application/x-www-form-urlencoded`
`Content-Length: ...`

Body:
`username=admin&password=admin`

Efecto práctico en pentesting ético:
GET → facilita enumeración y ataque directo por URL.
POST → fuerza a interceptar, editar body y entender formatos (form-data, JSON, XML).

El servidor decide según semántica. Una lectura debería ser GET. Una acción que cambie estado debería ser POST. En la práctica muchos desarrolladores mezclan, lo que abre superficie de ataque.
