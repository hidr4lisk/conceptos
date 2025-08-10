**Flashcard — Post-Shell Access (Linux & Windows)**

---

**Objetivo**: Escalar desde shell inestable/no interactiva a acceso persistente y completo.

---

**Linux**

1. **Buscar credenciales**:

   * Rutas comunes: `/home/<user>/.ssh` (claves SSH), archivos con contraseñas.
   * CTF: credenciales en texto plano en el sistema.
2. **Inyección de usuario**:

   * Vulnerabilidades como Dirty C0w, `/etc/passwd` o `/etc/shadow` escribibles.
   * Acceso posterior por SSH (si está abierto).

---

**Windows**

1. **Recuperar credenciales**:

   * Registro: contraseñas de servicios (VNC, etc.).
   * Archivos:

     * `C:\Program Files\FileZilla Server\FileZilla Server.xml`
     * `C:\xampp\FileZilla Server\FileZilla Server.xml`
     * Formato: MD5 o texto plano (según versión).
2. **Escalar a SYSTEM/Admin**:

   * Crear usuario y añadirlo a administradores:

     ```
     net user <username> <password> /add
     net localgroup administrators <username> /add
     ```
   * Acceso por: RDP, telnet, winexe, psexec, WinRM, etc.

---

**Clave**:

* **Reverse/Bind shells** → útiles para RCE inicial pero limitados.
* **Meta final** → acceso nativo estable (SSH en Linux, RDP/WinRM en Windows) para explotación avanzada.
