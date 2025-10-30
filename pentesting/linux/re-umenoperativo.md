### RESUMEN OPERATIVO

**Objetivo de la tarea**:
Configurar manualmente la resolución de nombres en tu máquina local para poder acceder correctamente a los sitios virtuales alojados en la máquina remota del laboratorio (máquina desplegada en TryHackMe), sin necesidad de un servidor DNS.

---

### PASOS CRÍTICOS

1. **Desplegar la máquina del laboratorio en TryHackMe**.
   Esto te dará una dirección IP única, necesaria para el archivo `hosts`.

2. **Editar el archivo `hosts` del sistema con privilegios de root/administrador**.

   * **Linux/macOS**:

     ```bash
     sudo nano /etc/hosts
     ```
   * **Windows** (con bloc de notas "Ejecutar como Administrador"):

     ```
     C:\Windows\System32\drivers\etc\hosts
     ```

3. **Agregar una sola línea al final** (reemplazando `MACHINE_IP` con la IP real de la máquina):

   ```txt
   10.10.123.123 overwrite.uploadvulns.thm shell.uploadvulns.thm java.uploadvulns.thm annex.uploadvulns.thm magic.uploadvulns.thm jewel.uploadvulns.thm demo.uploadvulns.thm
   ```

   * No debe haber líneas duplicadas con los mismos dominios.
   * Quitar la línea cuando termines o redespliegues la máquina.

4. **Evitar errores de conexión**:

   * No usar VPNs tipo Proton o Mullvad mientras usás el túnel de TryHackMe.
   * Verificar que no haya duplicados en el archivo `hosts`.

---

### CONCEPTO: ARCHIVO HOSTS

**Función**:
El archivo `hosts` es una tabla local de resolución de nombres que asocia direcciones IP con nombres de dominio. Se consulta antes que cualquier servidor DNS.

**Utilidad**:

* Emular servidores web locales o remotos.
* Acceder a sitios que usan *name-based virtual hosting* (un solo servidor responde por múltiples dominios según el encabezado HTTP `Host`).
* Controlar resolución de nombres sin depender de DNS (seguridad, pruebas, desarrollo, pentesting).

**Ejemplo práctico**:

```txt
127.0.0.1    localhost
10.10.123.123 demo.uploadvulns.thm
```

Cuando el navegador o `curl` accede a `demo.uploadvulns.thm`, el sistema no consulta DNS, sino que resuelve directamente a `10.10.123.123`.

---

### GLOSARIO

| Término                    | Definición Operativa                                                                           |
| -------------------------- | ---------------------------------------------------------------------------------------------- |
| `hosts` file               | Archivo plano que asocia dominios con IPs localmente                                           |
| DNS (Domain Name System)   | Sistema jerárquico para resolver dominios a IPs en Internet                                    |
| Name-based virtual hosting | Técnica para alojar múltiples sitios en una sola IP, diferenciados por nombre de dominio       |
| VHost (Virtual Host)       | Configuración en un servidor web (Apache/Nginx) que sirve contenido según el nombre de dominio |
| `MACHINE_IP`               | Dirección IP de la máquina desplegada en TryHackMe                                             |
| Entrada duplicada          | Dos o más líneas con los mismos dominios en el archivo `hosts` (causa conflicto)               |
| Resolución de nombres      | Proceso de traducir un nombre de dominio a una dirección IP                                    |
| Ruta `/etc/hosts`          | Ubicación estándar del archivo `hosts` en sistemas Unix-like                                   |
| Conexión VPN TryHackMe     | Red privada virtual usada para acceder al entorno aislado del laboratorio                      |
| Encabezado HTTP `Host`     | Campo en las solicitudes HTTP que indica el dominio solicitado                                 |

---

### NOTAS CRÍTICAS

* **El archivo `hosts` se prioriza sobre DNS**. Toda entrada aquí anula lo que diría un servidor de nombres.
* **Una mala configuración genera errores de conexión HTTP** (timeout, 404, 502, etc.).
* **Al reiniciar la máquina en THM, la IP cambia**. Requiere actualizar el archivo.

---
