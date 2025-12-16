**Flashcard — Prototype Pollution: herramientas clave**

**Frente**
Automatización de detección de Prototype Pollution en JavaScript / Node.js

**Reverso**

* **NodeJsScan**
  Escáner estático de seguridad para Node.js.
  Detecta múltiples vulnerabilidades, incluida prototype pollution.
  Uso típico: CI/CD, análisis de código fuente antes de deploy.

* **Prototype Pollution Scanner**
  Analiza codebases JavaScript buscando patrones vulnerables a pollution.
  Enfoque: detección estructural en lógica de merge, asignaciones profundas, parsers inseguros.

* **PPFuzz**
  Fuzzer específico para prototype pollution en aplicaciones web.
  Técnica: fuzzing de inputs que interactúan con propiedades de objetos (`__proto__`, `constructor`, `prototype`).
  Útil para encontrar sinks explotables dinámicamente.

* **Client-side detection (BlackFan)**
  Enfoque en JavaScript del lado cliente.
  Demuestra explotación de prototype pollution en navegador (XSS, comportamiento inesperado).
  Recurso clave para entender impacto real en frontend.

**Idea central**
Combinar análisis estático + fuzzing + pruebas client-side para cobertura completa de prototype pollution.
