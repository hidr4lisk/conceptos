No vas a mirar **a mano** los cientos de servicios. El truco es **filtrar antes de profundizar**.

---

### 1. Acotar por **cuenta de ejecución**

Los que interesan son los que corren como **cuentas privilegiadas**:

* `LocalSystem`
* `LocalService`
* `NetworkService`
* Usuarios de dominio con privilegios (ej: `NT AUTHORITY\SYSTEM`, `.\Administrador`, etc.).

En CMD, el `sc query` no te lo muestra. Tenés que complementarlo. Lo más rápido es usar **WMIC** (aunque deprecado sigue estando en Windows) o PowerShell.

#### CMD (WMIC):

```cmd
wmic service get Name,StartName,State,PathName
```

Eso ya te filtra en una sola vista:

* **StartName** = cuenta que lo ejecuta.
* **PathName** = binario.
* **State** = si está corriendo o no.

---

### 2. Acotar por **binarios sospechosos**

* Fijate si el `PathName` tiene espacios y no está entre comillas.
* Fijate si apunta a rutas fuera de `C:\Windows\System32\` o `C:\Program Files\` (instalaciones de terceros → más probables de ser inseguros).
* Fijate si el directorio es **writable** por usuarios bajos (`icacls`).

---

### 3. Acotar por **servicios que podés controlar**

Aunque un binario sea inseguro, si no podés **stop/start** o reconfigurar el servicio, no te sirve.
Revisá la **DACL del servicio**:

```cmd
sc sdshow <Servicio>
```

O más fácil, con Sysinternals `accesschk`:

```cmd
accesschk.exe -uws "Users" *
```

---

### Estrategia práctica

1. **Exportar lista con datos completos:**

   ```cmd
   wmic service get Name,StartName,State,PathName > servicios.txt
   ```
2. **Filtrar en el bloc de notas o con findstr**:

   * Buscar `LocalSystem`
   * Buscar `Program Files` (espacios sospechosos)
   * Buscar rutas que no tengan comillas
3. **Sobre esa sublista**, correr:

   ```cmd
   sc qc <Servicio>
   sc sdshow <Servicio>
   icacls "C:\ruta\binario.exe"
   ```

---

¿Querés que te arme un **workflow en CMD puro** (sin PowerShell) para exportar todo en un archivo y que solo te deje listos los servicios que corren como `LocalSystem` con rutas que tienen espacios?


No. No hace falta revisar todo uno por uno. El flujo correcto es **reducir la lista antes** y luego profundizar:

---

### Paso 1 — Exportar toda la info útil

En CMD:

```cmd
wmic service get Name,StartName,State,PathName > servicios.txt
```

Esto te da de un tirón:

* **Name** = lo que usarás con `sc qc`
* **StartName** = cuenta que lo ejecuta
* **PathName** = binario
* **State** = si está corriendo o no

---

### Paso 2 — Filtrar candidatos

* **StartName** → prioriza `LocalSystem`, `LocalService`, `NetworkService` o usuarios de dominio/admin.
* **PathName** → fijate:

  * Tiene espacios y no está entre comillas → posible *unquoted path*.
  * No apunta a `C:\Windows\System32\...` → binarios de terceros (más chances de permisos inseguros).
* **State** → servicios `STOPPED` son mejores porque podés iniciarlos a voluntad.

Ejemplo de filtro en CMD:

```cmd
findstr /I "LocalSystem" servicios.txt > candidatos.txt
findstr /I "Program Files" servicios.txt >> candidatos.txt
```

---

### Paso 3 — Profundizar en los sospechosos

Sobre los `Name` que te quedaron en `candidatos.txt`:

```cmd
sc qc <Servicio>
sc sdshow <Servicio>
icacls "C:\Ruta\al\binario.exe"
```

---

### Resultado

* De miles de líneas pasás a unas decenas.
* Solo ahí usás `sc qc` para confirmar `BINARY_PATH_NAME` y `SERVICE_START_NAME`.
* Solo en esos revisás permisos NTFS (`icacls`) y permisos de servicio (`sc sdshow`).

---

¿Querés que te escriba un **batch** que automatice: exportar servicios → filtrar por LocalSystem y rutas con espacios → dejarte listo un TXT con nombres de servicios candidatos?
