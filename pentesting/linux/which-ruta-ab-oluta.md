`which` = utilidad que muestra la **ruta absoluta** del ejecutable que se ejecutaría al llamar un comando.

Ejemplo:

```bash
which xfreerdp
```

Salida posible:

```
/usr/bin/xfreerdp
```

→ significa que el binario existe y está en el `PATH`.

Si no devuelve nada → el binario no está instalado o no está en el `PATH`.

Alternativas más completas:

```bash
command -v xfreerdp
type -a xfreerdp
```

¿Querés que te arme un bloque de comandos para verificar en una sola tirada si tenés `xfreerdp`, `rdesktop` y `remmina` instalados?
