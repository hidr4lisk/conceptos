**Componentes de una Web Application moderna (apunte resumido)**

---

### Arquitectura general

Las web apps modernas son **distribuidas**, no monolíticas. Separan responsabilidades y escalan por componentes.

---

### Componentes principales

**Front-end server**

* Reverse proxy / load balancer.
* Punto de entrada HTTP(S).
* Reenvía requests al back-end.
* Maneja TLS, headers, routing.

**Back-end server**

* Lógica de negocio.
* Procesa requests del usuario.
* Interactúa con databases y APIs.
* Tecnologías comunes: PHP, Python, JavaScript (Laravel, Django, Node.js).

**Databases**

* Almacenamiento persistente.
* SQL: MySQL, PostgreSQL.
* NoSQL: MongoDB, Redis, etc.

**APIs**

* Canal de comunicación front ↔ back.
* Integración con servicios externos.
* Normalmente REST o gRPC.
* Objetivo: desacoplamiento.

**Microservices**

* Servicios pequeños e independientes.
* Cada uno con función específica.
* Comunicación por red (HTTP/REST/gRPC).
* Ventajas: escalabilidad, aislamiento de fallos.
* Riesgo: mayor superficie de ataque.

---

### Load Balancers vs Reverse Proxies

**Load Balancer**

* Distribuye tráfico entre múltiples servidores.
* Evita sobrecarga de un nodo.
* Solo envía tráfico a servidores “healthy”.
* Mejora disponibilidad y tolerancia a fallos.
* Ejemplos: AWS ELB, HAProxy, F5.

**Reverse Proxy**

* Se ubica delante de los servidores web.
* Punto de acceso único.
* Reenvía requests al back-end adecuado.
* Puede hacer load balancing, pero no es su función primaria.
* Funciones extra: caching, auth, rate limiting.
* Ejemplos: NGINX, Apache mod_proxy, Varnish.

**Relación**

* En la práctica, muchos load balancers son reverse proxies.
* NGINX/HAProxy suelen cumplir ambos roles.

---

### Caching (rendimiento y escalabilidad)

**Objetivo**

* Reducir latencia.
* Disminuir carga en back-end y databases.

**Tipos**

**Content caching**

* Archivos estáticos (images, CSS, JS).
* Reduce requests repetidas al servidor.

**Database query caching**

* Cachea resultados de queries frecuentes.
* Menos I/O y CPU en la database.

**Full-page caching**

* Cachea páginas completas renderizadas.
* Útil en sitios de alto tráfico.

**Edge caching / CDNs**

* Cacheo cercano al usuario final.
* Menor latencia global.
* Ejemplos: Cloudflare, Akamai.

**API caching**

* Cachea responses de endpoints repetidos.
* Reduce procesamiento del back-end.

**Riesgo**

* Cache mal gestionado → contenido stale.
* Relevante para pentesting: inconsistencias, bypass de auth, cache poisoning.

---

### Idea clave para seguridad

* Más componentes = más superficie de ataque.
* Reverse proxies, caches y APIs suelen ser puntos críticos (headers, routing, trust boundaries).
* Microservices introducen nuevos vectores internos (SSRF, auth inter-service, misconfig).

---
