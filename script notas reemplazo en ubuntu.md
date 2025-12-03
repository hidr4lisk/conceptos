# Flashcard — Script reemplazo (Wayland)

---

## Frente — Pregunta

¿Cómo crear un script que lea el portapapeles, lo inserte en la plantilla y copie el resultado nuevamente al portapapeles en Wayland?

---

## Reverso — Respuesta (instrucciones mínimas y reproducibles)

**Archivo**: `~/scripts/reemplazo.sh`

**Contenido**:

```bash
#!/bin/bash

# Leer texto del portapapeles (Wayland)
texto=$(wl-paste | tr -d '\n')

# Si el portapapeles está vacío, avisar y salir
if [ -z "$texto" ]; then
  notify-send "Portapapeles vacío" "Copiá el texto a reemplazar y volvé a ejecutar." && exit 1
fi

# Aplicar la plantilla
resultado="Me dirijo a Ud. en atención a la nota $texto, con relación a la referencia, la misma se acompaña asociada a la presente para su conocimiento."

# Copiar resultado al portapapeles (Wayland)
echo -n "$resultado" | wl-copy

# Notificación
notify-send "Texto reemplazado" "Plantilla copiada al portapapeles"
```

**Permisos**:

```bash
chmod +x ~/scripts/reemplazo.sh
```

**Dependencias (instalar si falta)**:

```bash
sudo apt install wl-clipboard libnotify-bin
```

**Command para usar en lanzador/atajo**:

```
/home/<usuario>/scripts/reemplazo.sh
```

(Sustituir `<usuario>` por el nombre retornado por `whoami`; alternativa segura: `bash /home/<usuario>/scripts/reemplazo.sh`)

**Uso**:

1. Copiar el texto que querés insertar en la plantilla (Ctrl+C).
2. Hacer clic en el lanzador o usar el atajo de teclado.
3. Pegar (Ctrl+V) el texto con la plantilla aplicada.

---

## Nota técnica (opcional)

* El `tr -d '\n'` elimina saltos de línea para insertar el texto en una sola línea.
* La validación evita sobrescribir el portapapeles con una cadena vacía.
* Si querés soporte para X11 y Wayland en el mismo script, agrego la versión combinada.

---

Fin de la flashcard.
