**Explicación técnica estructurada sobre WPScan y sus funciones de enumeración:**

---

### 1. **Enumeración de Temas (`--enumerate t`)**

#### Mecanismo:

WPScan analiza rutas conocidas como:

```
/wp-content/themes/<nombre-del-tema>/
```

y verifica archivos o recursos cargados desde esa ubicación.

#### Técnica manual equivalente:

* Abrir el sitio en navegador.
* Ir a pestaña "Network" en DevTools.
* Identificar recursos CSS o JS dentro de `/themes/<tema>/assets/`.

#### Comando:

```bash
wpscan --url http://target.com --enumerate t
```

#### Resultado:

* Devuelve nombre del tema activo.
* Indica método de descubrimiento (e.g., "Known locations").

---

### 2. **Enumeración de Plugins (`--enumerate p`)**

#### Mecanismo:

Busca rutas como:

```
/wp-content/plugins/<nombre-del-plugin>/
```

Verifica existencia y archivos como `readme.txt` para identificar versión.

#### Condición explotada:

* Directory Listing habilitado.
* Plugins sin archivo `index.*` en el directorio.

#### Comando:

```bash
wpscan --url http://target.com --enumerate p
```

#### Resultado:

* Lista plugins instalados.
* En algunos casos también devuelve la versión (si `readme.txt` está accesible).

---

### 3. **Enumeración de Usuarios (`--enumerate u`)**

#### Mecanismo:

* WordPress asigna URLs predecibles a autores:

```
/?author=1
```

* Redirecciona a:

```
/author/<username>
```

WPScan automatiza esta detección mediante pruebas secuenciales de IDs de autores.

#### Comando:

```bash
wpscan --url http://target.com --enumerate u
```

#### Resultado:

* Devuelve lista de nombres de usuario válidos (autores).

---

### 4. **Enumeración de Vulnerabilidades (`--enumerate v`)**

#### Requiere:

* API Key de [WPVulnDB](https://wpvulndb.com)
* Añadirla en configuración de WPScan (`~/.wpscan/cli_options.json`)

#### Ejemplo:

```bash
wpscan --url http://target.com --enumerate vp
```

* `v` = buscar vulnerabilidades.
* `p` = aplicar sobre plugins.

#### Resultado:

* Lista plugins + versiones + vulnerabilidades conocidas.

---

### 5. **Ataque por Fuerza Bruta (`--passwords`, `--usernames`)**

#### Requisitos:

* Lista de usuarios válidos (`--enumerate u`)
* Diccionario de contraseñas (ej: `rockyou.txt`)

#### Comando:

```bash
wpscan --url http://target.com --usernames usuario1 --passwords rockyou.txt
```

#### Resultado:

* Intenta login con cada combinación.
* Devuelve credenciales válidas si encuentra alguna.

---

### 6. **Modos de Detección (`--plugins-detection`)**

Por defecto, WPScan usa detección pasiva. Para aumentar cobertura:

#### Comando:

```bash
wpscan --url http://target.com --enumerate p --plugins-detection aggressive
```

#### Modos disponibles:

* `passive`
* `mixed`
* `aggressive`

Más agresividad = más solicitudes HTTP = mayor probabilidad de activación de WAF.

---

### 7. **Resumen de Flags Clave**

| Flag                          | Función                           | Ejemplo completo                                                 |
| ----------------------------- | --------------------------------- | ---------------------------------------------------------------- |
| `--enumerate p`               | Enumerar plugins                  | `wpscan --url <target> --enumerate p`                            |
| `--enumerate t`               | Enumerar temas                    | `wpscan --url <target> --enumerate t`                            |
| `--enumerate u`               | Enumerar usuarios                 | `wpscan --url <target> --enumerate u`                            |
| `--enumerate vp`              | Plugins + vulnerabilidades        | `wpscan --url <target> --enumerate vp`                           |
| `--plugins-detection`         | Nivel de agresividad de detección | `--plugins-detection aggressive`                                 |
| `--usernames` + `--passwords` | Fuerza bruta de credenciales      | `wpscan --url <target> --usernames user --passwords rockyou.txt` |

---

**Notas operativas:**

* WPScan no es anónimo. Usar proxy como Burp o Tor si se requiere evasión.
* Uso agresivo puede activar mecanismos de defensa automática (WAF, rate-limiting, bloqueo por IP).
* No requiere autenticación salvo para escaneo de sitios protegidos por login.

---