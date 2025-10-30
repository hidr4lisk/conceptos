**Flashcard**

**Tema:** Password Reset Flow Vulnerabilities

**Conceptos Clave:**

* **Email Reset:** Envío de token o link a correo. Depende de la seguridad del email.
* **Security Questions:** Basado en respuestas preconfiguradas. Débil si las respuestas son fáciles de adivinar.
* **SMS Reset:** Token por SMS. Vulnerable a SIM swapping/interceptación.

**Vulnerabilidades:**

* **Predictable Tokens:** Tokens con patrones simples/brute-forceables.
* **Token Expiration Issues:** Tokens que no expiran rápido → ventana de ataque.
* **Insufficient Validation:** Verificación de identidad débil (preguntas triviales, correo comprometido).
* **Information Disclosure:** Errores que confirman usuarios válidos → enumeración.
* **Insecure Transport:** Tokens enviados por HTTP → sniffing.

**Ejemplo Exploitable (TryHackMe – Predictable Tokens Lab):**

```php
$token = mt_rand(100, 200);   // 3 dígitos predecibles
```

* Brute force con **Crunch**:

```bash
crunch 3 3 -o otp.txt -t %%% -s 100 -e 200
```

* Cargar lista en **Burp Intruder** sobre parámetro `token`.
* Identificar respuesta con mayor `Content-Length` = token válido.

**Mitigaciones:**

* Tokens aleatorios criptográficamente seguros.
* Expiración corta y un solo uso.
* Evitar mensajes de error que confirmen usuarios.
* HTTPS obligatorio.
* MFA como capa adicional.
