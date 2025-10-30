¡Entiendo! El **MATE Terminal** de Parrot es bastante funcional, pero tiene un diseño y características que no a todos les gustan. Si prefieres el **gnome-terminal** de Kali, es totalmente posible instalarlo en Parrot para que tengas una experiencia similar.

Aquí tienes los pasos para cambiarlo:

### 1. Instalar **gnome-terminal**:

Abre un terminal y ejecuta el siguiente comando para instalar **gnome-terminal**:

```bash
sudo apt update
sudo apt install gnome-terminal
```

### 2. Cambiar el terminal predeterminado:

Una vez que hayas instalado **gnome-terminal**, puedes configurarlo como el terminal predeterminado en Parrot.

Para hacerlo, ejecuta el siguiente comando:

```bash
sudo update-alternatives --config x-terminal-emulator
```

Esto te mostrará una lista de terminales disponibles. Aquí verás algo similar a:

```text
Selection    Path               Priority   Status
------------------------------------------------------------
0            /usr/bin/gnome-terminal  40      auto mode
1            /usr/bin/mate-terminal   30      manual mode
2            /usr/bin/gnome-terminal  40      manual mode
```

En este caso, selecciona el número correspondiente al **gnome-terminal** (probablemente el "2"), presionando la tecla correspondiente y luego **Enter**.

### 3. Cerrar y abrir el terminal:

Una vez hecho esto, el próximo terminal que abras debería ser **gnome-terminal**.

---