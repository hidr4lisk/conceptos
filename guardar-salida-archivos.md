Redirigí la salida estándar a un archivo con `>` o `>>`.

Ejemplos:

**Sobrescribir archivo (crea o reemplaza):**

```bash
nikto --list-plugins > plugins.txt
```

```bash
nikto --list-plugins > plugins.md
```

**Anexar al final de un archivo existente:**

```bash
nikto --list-plugins >> plugins.txt
```

Si querés guardar también los errores (`stderr`) en el mismo archivo:

```bash
nikto --list-plugins > plugins.txt 2>&1
```
