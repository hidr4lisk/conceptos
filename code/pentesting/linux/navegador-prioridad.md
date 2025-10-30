### Flashcard: Control del navegador predeterminado en Linux

**Conceptos clave**

* `x-www-browser`: enlace simbólico gestionado por `update-alternatives` que define el navegador por defecto en sistemas Linux (independiente del entorno gráfico). Muchas apps CLI o basadas en `xdg-open` lo usan para abrir URLs.
* `gnome-www-browser`: equivalente específico para entornos basados en GNOME. Algunas aplicaciones de GNOME consultan este link en lugar de `x-www-browser`.
* Ambos son “alternatives” administrados por Debian/Ubuntu mediante `update-alternatives`, con prioridades numéricas.

**Problema común**
Si hay más de un navegador instalado (ej. Firefox y Chromium) y tienen la misma prioridad, el sistema puede lanzar cualquiera en modo automático. Eso genera inconsistencias (ej. VS Code abre Chromium aunque el usuario use Firefox).

**Solución**
Forzar Firefox como navegador predeterminado elevando su prioridad y activándolo en modo automático.

**Comandos**

1. Ver estado actual:

```bash
update-alternatives --display x-www-browser
update-alternatives --display gnome-www-browser
```

2. Registrar Firefox con prioridad 100:

```bash
sudo update-alternatives --install /usr/bin/x-www-browser x-www-browser /usr/bin/firefox 100
sudo update-alternatives --install /usr/bin/gnome-www-browser gnome-www-browser /usr/bin/firefox 100
```

3. Volver a modo automático para que gane la prioridad mayor:

```bash
sudo update-alternatives --auto x-www-browser
sudo update-alternatives --auto gnome-www-browser
```

4. Confirmar:

```bash
update-alternatives --display x-www-browser
update-alternatives --display gnome-www-browser
```

**Resultado esperado**

* Firefox queda con prioridad 100.
* Chromium con 40.
* En modo automático siempre se elegirá Firefox.

---

¿Querés que arme otra flashcard similar pero para el caso de **variables de entorno** (`$BROWSER`) que también pueden forzar qué navegador abre VS Code o cualquier otra app?
