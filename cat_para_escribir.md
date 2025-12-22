# Servidor receptor minimalista:

```
cat > server.py << 'EOF'
from http.server import SimpleHTTPRequestHandler, HTTPServer

class H(SimpleHTTPRequestHandler):
    def do_POST(self):
        l = int(self.headers['Content-Length'])
        d = self.rfile.read(l).decode()
        with open('data.html','a') as f:
            f.write(d+'\n')
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

HTTPServer(('',8080), H).serve_forever()
EOF

python3 server.py

```

Porque **`cat` se usa como mecanismo de escritura**, no por su funci�n original de mostrar archivos.

Explicaci�n directa.

---

## Qu� hace `cat` realmente aqu�

```
cat > server.py << 'EOF'
```

No se est� usando `cat` para leer nada.

Se est� usando porque:

* `cat` **lee stdin**
* `>` redirige stdout a un archivo
* el *here-document* alimenta stdin

Resultado:

```
stdin (texto del script)
\u2192 cat
\u2192 stdout
\u2192 server.py
```

---

## Por qu� no `nano`, `vim` o `echo`

### `nano` / `vim`

* Interactivos
* No reproducibles
* No automatizables
* No aptos para copiar/pegar en labs

### `echo`

* Mala idea para bloques grandes
* Problemas con:

  * saltos de l�nea
  * comillas
  * caracteres especiales
* Ilegible y fr�gil

Ejemplo malo:

```
echo "linea1\nlinea2\n..." > server.py
```

---

## Por qu� `cat << EOF` es la opci�n correcta

Ventajas t�cnicas:

* No interactivo
* Reproducible
* Copy-paste seguro
* Respeta el contenido exacto
* Usado en scripts, CTFs y writeups reales

Con `'EOF'`:

* No se expanden variables (`$VAR`)
* No se ejecutan comandos (`$(...)`)
* El contenido es literal

---

## Alternativa equivalente (para que lo veas claro)

Esto es **lo mismo**:

```
cat << 'EOF' > server.py
<contenido>
EOF
```

Solo cambia el orden de la redirecci�n.

---

## Mental model

Piensa esto:

```
cat = "copiadora"
EOF = "documento fuente"
> server.py = "archivo destino"
```

Nada m�s.

---

## En contexto SSRF / labs

`cat << EOF` es est�ndar porque:

* Permite crear payloads r�pido
* No rompe shells remotos
* Funciona igual en Kali, AttackBox, Docker, VPS

Por eso se usa.
No es por estilo. Es por **control y reproducibilidad**.
