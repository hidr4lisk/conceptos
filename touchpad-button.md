---

**Flashcard: Toggle Touchpad en Kali XFCE**

---

**1. Identificar touchpad**

```bash
xinput list
```

Busca dispositivo con nombre similar a "Touchpad", anota exacto.

---

**2. Script toggle `/usr/local/bin/toggle-touchpad.sh`**

```bash
#!/bin/bash
DEVICE="NOMBRE_TOUCHPAD"
STATE=$(xinput list-props "$DEVICE" | grep "Device Enabled" | awk '{print $4}')
if [ "$STATE" -eq 1 ]; then
    xinput disable "$DEVICE"
    notify-send -t 2000 "Touchpad OFF"
else
    xinput enable "$DEVICE"
    notify-send -t 2000 "Touchpad ON"
fi
```

Reemplaza `NOMBRE_TOUCHPAD` por el nombre exacto.

---

**3. Permisos ejecución**

```bash
sudo chmod +x /usr/local/bin/toggle-touchpad.sh
```

---

**4. Crear botón lanzador en XFCE**

* Click derecho en barra → Panel → Añadir nuevo elemento → Botón lanzador personalizado.
* En "Comando" poner:

```bash
/usr/local/bin/toggle-touchpad.sh
```

* Elegir ícono representativo.

---

**Resultado:**

Botón en barra que activa/desactiva touchpad con notificación visual ON/OFF.

---

Repetir proceso en otras PCs cambiando solo `DEVICE` según `xinput list`.
