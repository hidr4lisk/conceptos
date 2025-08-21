# Flashcard — Escalada de Privilegios en **Windows Services** (versión detallada)

---

## 0) Terminología mínima (operativa)

* **SCM (Service Control Manager):** núcleo que crea/inicia/detiene servicios y valida permisos.
* **Objeto “Servicio”:** metadatos clave:

  * `BINARY_PATH_NAME` (o `PathName`): ejecutable + argumentos.
  * `SERVICE_START_NAME` (o `StartName`): cuenta que ejecuta el servicio.
  * **Service DACL:** quién puede **consultar/cambiar** configuración del servicio.
* **Archivo/DACL de archivos y carpetas:** permisos NTFS sobre el EXE y cada directorio de su ruta.
* **`icacls`:** inspección/modificación de permisos NTFS.

  * Atajos comunes: `F=FullControl`, `M=Modify`, `RX=Read&Execute`, `R=Read`, `W=Write`.
  * Avanzados (frecuentes al auditar):
    `OI`=Object Inherit, `CI`=Container Inherit, `IO`=Inherit Only,
    `WD`=Write Data/Add File, `AD`=Append Data/Add Subdir, `X`=Execute, `DC`=Delete Child.
* **SDDL (Service DACL cruda):** cadena devuelta por `sc sdshow <svc>`. Da granularidad fina (quién puede `START/STOP/CHANGE_CONFIG`, etc.).

---

## 1) Dónde sacar **la lista de servicios** y metadatos clave

### CMD

```cmd
sc query type= service state= all
sc qc <Servicio>
sc sdshow <Servicio>       :: SDDL de la DACL del servicio
wmic service get Name,DisplayName,State,StartMode,StartName,PathName
```

### PowerShell (preferido)

```powershell
Get-CimInstance Win32_Service |
  Select Name,DisplayName,State,StartMode,StartName,PathName
```

---

## 2) Detección rápida por vector (en lote)

### 2.1 Unquoted Service Path (sin comillas + con espacios)

```powershell
Get-CimInstance Win32_Service |
 Where-Object { $_.PathName -and $_.PathName -notmatch '^"' -and $_.PathName -match ' ' } |
 Select Name, StartName, PathName
```

* Candidatos = servicios cuyo `PathName` no está entre comillas **y** contiene espacios.

### 2.2 Permisos inseguros en el **binario** o en **directorios** de la ruta

```powershell
# Extrae el EXE “real” (primera ruta hasta .exe) y evalúa NTFS
Get-CimInstance Win32_Service |
  ForEach-Object {
    if (-not $_.PathName) { return }
    $raw = $_.PathName.Trim('"')
    $exe = ($raw -split '\.exe',2)[0] + '.exe'
    if (Test-Path $exe) {
      Write-Host "`n[$($_.Name)] $exe"
      cmd /c "icacls `"$exe`""
      # Revisa también cada directorio ascendente (posibles puntos de inyección)
      $d = Split-Path $exe -Parent
      while ($d -and (Test-Path $d)) {
        Write-Host " Dir: $d"
        cmd /c "icacls `"$d`""
        $parent = Split-Path $d -Parent
        if ($parent -eq $d) { break } else { $d = $parent }
      }
    }
  }
```

* Señales de riesgo: **Users**/**Everyone** con `M` o `F` sobre el **EXE**; o `W/M/F` sobre **directorios** en la ruta (capacidad de soltar/ sustituir binarios).

### 2.3 Permisos inseguros en la **Service DACL** (cambiar config/arrancar como otro usuario)

```cmd
sc sdshow <Servicio>   :: inspección manual de SDDL
```

* Heurística: si un grupo no privilegiado (p.ej. `BUILTIN\Users`, `Authenticated Users`) tiene derechos que incluyen **CHANGE\_CONFIG** o **WRITE\_DAC**, es crítico.
* Alternativa con Sysinternals (si disponible en el host):

```cmd
accesschk.exe -uws "Users" *      :: lista servicios donde "Users" tiene escritura
accesschk.exe -uws "Everyone" *   :: idem para Everyone
```

> Nota: `accesschk` simplifica “quién puede escribir en el servicio”. Usa `accesschk.exe /?` si necesitas ver banderas disponibles en esa versión.

---

## 3) Validación de hallazgos (causa → efecto)

1. **Unquoted Path**

   * Causa: `PathName` sin comillas + espacios.
   * Efecto: el SCM resuelve en orden progresivo (“C:\Program.exe”, “C:\Program Files...”, etc.).
   * Explotabilidad real requiere **escritura** en algún directorio candidato de esa cadena de resolución.
   * Validación mínima:

     ```powershell
     $p='C:\Program Files\Vendor App\bin\svc.exe -k arg'
     # Candidatos de búsqueda del SCM (ejemplo manual):
     "C:\Program.exe","C:\Program Files\Vendor.exe","C:\Program Files\Vendor App\bin\svc.exe"
     # Comprobar escritura:
     cmd /c 'icacls "C:\Program Files"'        # normalmente NO writable
     cmd /c 'icacls "C:\Program"'              # si existe y es writable ⇒ riesgo alto
     ```

2. **Executable Permissions**

   * Causa: `icacls` muestra `F` o `M` para **Users/Everyone** en el **EXE** o `W/M/F` en directorios de su ruta.
   * Efecto: sustitución/plantado de binario o DLL hijacking según carga.
   * Validación mínima:

     ```cmd
     icacls C:\Path\service.exe
     icacls "C:\Path con espacios"
     ```
   * Interpretación rápida:

     * `F`/`M` en EXE para Users/Everyone ⇒ **crítico**.
     * En directorios: presencia de `WD`/`AD` o `M`/`F` ⇒ **crítico** (posible drop).

3. **Service DACL**

   * Causa: DACL del servicio concede a usuarios no admin derechos de **cambio de configuración** o **inicio/parada**.
   * Efecto: posibilidad de redirigir `binPath` o manipular arranque (según privilegios exactos).
   * Validación mínima:

     ```cmd
     sc sdshow <Servicio>   :: revisar ACEs con permisos de WRITE/CHANGE_CONFIG para grupos bajos
     ```
   * Con `accesschk`:

     ```cmd
     accesschk.exe -uws "Authenticated Users" *
     ```

---

## 4) Lectura de **icacls** (mapa mínimo)

| Marca | Significado práctico                    |
| ----: | --------------------------------------- |
|   `F` | FullControl                             |
|   `M` | Modify                                  |
|  `RX` | Read & Execute                          |
|   `R` | Read                                    |
|   `W` | Write                                   |
|  `WD` | Write Data / Add File (drop de archivo) |
|  `AD` | Append Data / Add Subdir (dir)          |
|  `OI` | Heredar a archivos                      |
|  `CI` | Heredar a carpetas                      |
|  `IO` | Solo heredado                           |

Interpretación operativa: presencia de `F` o `M` para **Users/Everyone** en binario/directorio ⇒ alto riesgo de sustitución/plantado.

---

## 5) Flujos de trabajo (auditoría reproducible)

### 5.1 Inventario completo + export

```powershell
Get-CimInstance Win32_Service |
  Select Name,StartName,State,StartMode,PathName |
  Export-Csv services.csv -NoTypeInformation -Encoding UTF8
```

### 5.2 Candidatos “unquoted + espacios”

```powershell
Get-CimInstance Win32_Service |
 Where-Object { $_.PathName -and $_.PathName -notmatch '^"' -and $_.PathName -match ' ' } |
 Select Name,StartName,PathName
```

### 5.3 Comprobación de permisos NTFS sobre EXE y cadenas de directorios

```powershell
$targets = Get-CimInstance Win32_Service | Where-Object { $_.PathName }
foreach($s in $targets){
  $raw = $s.PathName.Trim('"')
  $exe = ($raw -split '\.exe',2)[0] + '.exe'
  if(Test-Path $exe){
    "`n[EXE] $($s.Name) :: $exe"
    cmd /c "icacls `"$exe`""
    # Chequear árbol de directorios ascendentes
    $d = Split-Path $exe -Parent
    while($d){
      "  [DIR] $d"
      cmd /c "icacls `"$d`""
      $p = Split-Path $d -Parent
      if($p -eq $d){break}; $d = $p
    }
  }
}
```

### 5.4 Revisión de **Service DACL** en servicios sospechosos

```powershell
# Lista servicios que NO corren como el usuario actual y por tanto serían interesantes
Get-CimInstance Win32_Service |
 Where-Object { $_.StartName -match 'LocalSystem|LocalService|NetworkService' } |
 Select Name,StartName,PathName

# SDDL por servicio
sc.exe sdshow <Servicio>
```

Con Sysinternals:

```cmd
accesschk.exe -uws "Users" *
accesschk.exe -uws "Everyone" *
```

---

## 6) Explotabilidad (alto nivel, para laboratorio)

* **Executable Permissions:** si un usuario no privilegiado puede **escribir/sustituir** el EXE o **soltar un EXE** en un directorio de la ruta, al **reiniciar**/arrancar el servicio el código se ejecutará con la **cuenta del servicio** (`StartName`).
* **Unquoted Path:** si no hay comillas y hay un directorio **escribible** en la cadena de resolución progresiva, el primer nombre coincidente será cargado al arrancar el servicio.
* **Service DACL:** si la DACL permite **cambiar configuración** a usuarios bajos, pueden **redirigir** el `binPath` o alterar arranque. El impacto depende de la cuenta efectiva de ejecución configurada.

> Límite intencional: sin pasos de sustitución ni generación de payload en este documento. Usa únicamente en entornos de laboratorio controlados.

---

## 7) Remediación (para cerrar hallazgos durante hardening)

* **Citar rutas** en `BINARY_PATH_NAME` (comillas dobles completas).
* Ajustar NTFS: retirar `M/F/W` para **Users/Everyone** en EXEs y directorios de programa.
* Endurecer **Service DACL**: restringir a Administrators/Service Admins la capacidad de `CHANGE_CONFIG/START/STOP`.
* Instalar servicios en rutas no escribibles por usuarios estándar.

---

## 8) Checklist final (operativo)

1. Enumerar: `Get-CimInstance Win32_Service | Select Name,StartName,PathName`.
2. Unquoted+espacios: filtro PowerShell anterior.
3. NTFS sobre EXE y directorios ascendentes: `icacls`.
4. DACL del servicio: `sc sdshow <svc>` (+ `accesschk.exe -uws "Users" *` si disponible).
5. Clasificar riesgo: ¿Users/Everyone con `M/F/W`? ¿StartName elevado (LocalSystem/Service)? ¿Servicio auto/arrancable?

---

## 9) Notas precisas

* En PowerShell, usa **`sc.exe`** (no `sc`) para evitar el alias `Set-Content`.
* `wmic` está deprecado, pero útil en hosts antiguos.
* `accesschk` no viene por defecto; si no está presente, apóyate en `sc sdshow` y `Get-Acl` sobre la clave `HKLM:\SYSTEM\CurrentControlSet\Services\<Servicio>` para corroborar permisos de configuración vía registro.

---

Este documento prioriza **detección, validación e interpretación**. Para pruebas de ejecución en laboratorio, deriva los pasos desde la condición detectada, respetando políticas de tu entorno.
