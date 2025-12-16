**Flashcard \u2014 Prototype Pollution: Mitigaci�n**

**Frente**
Mitigaci�n de Prototype Pollution
Enfoque Pentesting y Secure Coding

**Dorso**

**Pentesters**

* Input fuzzing sobre estructuras basadas en prototipos (`__proto__`, `constructor`, `prototype`)
* An�lisis de contexto: rastrear c�mo inputs llegan a merges/clones (`Object.assign`, `lodash.merge`, custom merge)
* Inyecci�n de payloads en flujos protot�picos
* Evaluaci�n de CSP: intento de bypass + payloads que modifiquen prototipos
* An�lisis de dependencias: librer�as desactualizadas con PP conocida
* Static Code Analysis: detecci�n de patrones inseguros en fase temprana

**Secure Code Developers**

* Evitar `__proto__`; usar `Object.getPrototypeOf()`
* Objetos inmutables cuando sea posible (`Object.freeze`)
* Encapsulaci�n: exponer solo interfaces necesarias
* Defaults seguros: no derivar prototipos desde input usuario
* Sanitizaci�n y validaci�n estricta de inputs
* Gesti�n de dependencias: updates + monitoreo de CVEs
* Security Headers: CSP para limitar carga de scripts maliciosos

**Idea clave**
La mitigaci�n efectiva combina testing agresivo + patrones de c�digo seguros + control de dependencias. Prototype Pollution es efecto sist�mico, no bug aislado.
