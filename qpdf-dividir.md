Flashcard concisa sobre lo que hiciste con **qpdf**:

---

**Herramienta:** `qpdf`
**Uso:** dividir un PDF en rangos de páginas específicos.

**Instalación (Debian/Ubuntu/Kali/Parrot):**

```bash
sudo apt update
sudo apt install qpdf -y
```

**Sintaxis general:**

```bash
qpdf archivo.pdf --pages archivo.pdf INICIO-FIN -- salida.pdf
```

**Ejemplo aplicado (informe.pdf):**

```bash
qpdf informe.pdf --pages informe.pdf 1-1242 -- parte1.pdf
qpdf informe.pdf --pages informe.pdf 1243-2416 -- parte2.pdf
qpdf informe.pdf --pages informe.pdf 2417-3375 -- parte3.pdf
```

**Clave:**

* `--pages` indica qué rangos extraer.
* Se puede usar `z` como última página.
* Genera PDFs separados con los cortes definidos.

---
