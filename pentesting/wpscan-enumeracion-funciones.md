**FLASHCARD COMPLETA – WPScan: Detección de Temas, Plugins, Usuarios y Vulnerabilidades**

---

### **1. Enumerar el *theme activo***

**Técnica manual:**

* Abrir navegador → F12 → pestaña **Network**
* Visitar sitio → buscar URLs con `/wp-content/themes/<nombre>`
* Ejemplo:
  `http://target/wp-content/themes/twentytwentyone/assets/` → theme activo = `twentytwentyone`

**Técnica automatizada:**

```bash
wpscan --url http://target/ --enumerate t
```

* Detecta el *theme activo* usando rutas conocidas.
* Ejemplo: detecta `twentytwenty` porque encontró su carpeta en `/wp-content/themes/`.

---

### **2. Enumerar *plugins instalados***

**Técnica por listado de directorio:**

* Si el servidor permite *Directory Listing* y no hay `index.html` o `index.php`, muestra los archivos de `/wp-content/plugins/`.

**Técnica automatizada:**

```bash
wpscan --url http://target/ --enumerate p
```

* Detecta plugins conocidos por nombre de carpeta, archivos, assets embebidos y `README.txt`
* Ejemplo: detecta `easy-table-of-contents`, extrae su versión desde `/wp-content/plugins/easy-table-of-contents/readme.txt`

---

### **3. Enumerar *usuarios (autores)***

**Técnica automatizada:**

```bash
wpscan --url http://target/ --enumerate u
```

* Extrae usernames de los autores de posts.

---

### **4. Detectar *vulnerabilidades***

**Requiere configurar WPScan con API key de WPVulnDB**
**Comando:**

```bash
wpscan --url http://target/ --enumerate vp
```

* `v` = Vulnerabilidades
* `p` = Plugins (puede combinarse con `t`, `u`, etc.)

---

### **5. Ataque de contraseñas (bruteforce)**

**Comando:**

```bash
wpscan --url http://target/ --usernames <usuario> --passwords rockyou.txt
```

* Requiere lista de usuarios previa (`--enumerate u`)

---

### **6. Ajustar *nivel de detección/agresividad***

**Plugins detection pasiva (default) o agresiva (más ruidosa):**

```bash
wpscan --url http://target/ --enumerate p --plugins-detection aggressive
```

* Riesgo de detección por WAF o firewall si no se ajusta correctamente.

---

### **7. Resumen de flags WPScan**

| Flag                             | Función                                  | Ejemplo completo                               |
| -------------------------------- | ---------------------------------------- | ---------------------------------------------- |
| `p`                              | Enumerar plugins                         | `--enumerate p`                                |
| `t`                              | Enumerar theme activo                    | `--enumerate t`                                |
| `u`                              | Enumerar nombres de usuario (autores)    | `--enumerate u`                                |
| `v`                              | Vulnerabilidades (requiere WPVulnDB API) | `--enumerate vp`                               |
| `--plugins-detection aggressive` | Perfil agresivo para detectar plugins    | `--enumerate p --plugins-detection aggressive` |

---

What is the name of the other aggressiveness profile that we can use in our WPScan command?

    passive


