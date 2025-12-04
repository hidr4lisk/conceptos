 Let’s install the bugcrowd HUNT extensions for OWASP ZAP. This will passively scan for known vulnerabilities in web applications.


First navigate in your terminal somewhere you’d like to store the scripts

` git clone https://github.com/bugcrowd/HUNT `


Then in ZAP click the “Manage Add-Ons” icon


From the Marketplace install “Python Scripting” and “Community Scripts”


In ZAP Options, under Passive Scanner, make sure “Only scan messages in scope” is enabled. Then hit OK.



In ZAP open the Scripts tab.

And under Passive Rules, find and enable the HUNT.py script


Now when you browse sites and HUNT will passively scan for SQLi, LFI, RFI, SSRF, and others. Exciting!


Procedimiento mínimo, directo y reproducible para Kali (paquete oficial de ZAP):

---

# 1. Abrir el script de arranque de ZAP

```
sudo nano /usr/share/zaproxy/zap.sh
```

Ese archivo ejecuta ZAP y es donde se declaran variables para la JVM.

---

# 2. Insertar los límites de memoria de Java

Justo **antes** de la línea que contiene `exec`, agregar:

```
export JAVA_OPTS="-Xms512m -Xmx1500m"
```

Estructura esperada:

```
# ...contenido previo del script...

export JAVA_OPTS="-Xms512m -Xmx1500m"

exec /usr/lib/jvm/default-java/bin/java $JAVA_OPTS -jar "$ZAP_INSTALL/zap.jar" "$@"
```

El orden es crítico: la variable debe existir **antes** del `exec`.

---

# 3. Guardar

En nano:

```
Ctrl+O
Enter
Ctrl+X
```

---

# 4. Reiniciar ZAP desde el menú o con:

```
zap.sh
```

Asegurate de no lanzarlo desde otro launcher que ignore el script.

---

# 5. Verificación

## Opción A: desde ZAP

```
Help → About → JVM
```

Debe mostrar:

```
Max memory ≈ 1500 MB
```

## Opción B: consola

```
ps aux | grep java
```

Debe verse:

```
-Xms512m -Xmx1500m
```

---

Con esto ZAP queda limitado y no podrá consumir más de ~1.5 GB, evitando cuelgues en VM de 4–6 GB.
