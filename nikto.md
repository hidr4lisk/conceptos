**Flashcard – Nikto**

**Definition:**
Open-source, feature-rich web server vulnerability scanner released in 2001.

**Capabilities:**

* Scans all types of web servers (not app-specific like WPScan).
* Detects:

  * Sensitive files
  * Outdated servers/programs
  * Common misconfigurations (directory indexing, CGI scripts, missing XSS protections)

**Installation:**

* **Kali/Parrot (latest):** Pre-installed
* **Older Kali:**

  ```bash
  sudo apt update && sudo apt install nikto
  ```
* **Other Debian/Ubuntu:** Follow developer installation guide


**Nikto Advanced Usage**

**Basic Scan:**

* Command:

  ```bash
  nikto -h <IP_or_Domain>
  ```
* Retrieves HTTP headers, detects sensitive files/directories.
* Identifies server type via artefacts (e.g., favicon, default paths).
* Detects risky HTTP methods (PUT, DELETE).

**Multiple Hosts & Ports:**

* From Nmap scan:

  ```bash
  nmap -p80 172.16.0.0/24 -oG - | nikto -h -
  ```
* Multiple ports on one host:

  ```bash
  nikto -h 10.10.10.1 -p 80,8000,8080
  ```

**Plugins:**

* List:

  ```bash
  nikto --list-plugins
  ```
* Examples:

  * `apacheusers` → enumerate Apache HTTP Auth users
  * `cgi` → search for exploitable CGI scripts
  * `robots` → analyse `robots.txt`
  * `dir_traversal` → attempt LFI
* Use plugin:

  ```bash
  nikto -h 10.10.10.1 -Plugin apacheuser
  ```

**Verbosity (-Display):**

* `1` → show redirects
* `2` → show cookies
* `E` → show errors

**Tuning (-Tuning):**

* `0` → file upload points
* `2` → misconfigurations/default files
* `3` → information disclosure
* `4` → injection points (XSS/HTML)
* `8` → command execution points
* `9` → SQL injection points

**Saving Output:**

* Command:

  ```bash
  nikto -h http://IP -o report.html
  ```
* Formats: `.txt`, `.html` (auto-detected by extension or set with `-f`).


**Flashcard – Escaneo completo de puertos HTTP para un host con Nmap + Nikto**

**Flujo manual:**

1. Escanear todos los puertos y detectar servicios:

```bash
nmap -p- --open -sV 100.100.100.100
```

2. Identificar puertos HTTP/HTTPS en el resultado.
3. Pasar esos puertos a Nikto:

```bash
nikto -h 100.100.100.100 -p <lista_puertos>
```

**Banderas usadas en el ejemplo automático anterior:**

* `-p-` → Escanea todos los puertos (1-65535).
* `--open` → Muestra solo puertos abiertos.
* `-sV` → Detecta el servicio y versión en cada puerto.
* `--script=http-title` → Ejecuta script NSE para extraer el título HTTP (rápida confirmación de puertos web).
* `-oG -` → Salida en formato “grepable” enviada a `stdout` (guion `-` = no guarda en archivo).
* `grep -i 'http'` → Filtra líneas que contienen servicios HTTP (no lo usarías si lo haces manual).
* `awk '{print $2":"$4}'` → Extrae IP y puerto.
* `sed 's/\/open//g'` → Limpia el texto “/open” del puerto.
* `nikto -h -` → Nikto lee la lista `host:port` desde `stdin`.
