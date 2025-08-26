### Flashcard: Herramientas de Enumeración para Escalación de Privilegios en Windows

**Frente:**
¿Cuáles son las herramientas comunes para identificar vectores de escalación de privilegios en Windows y cómo se usan?

**Reverso:**
**1. WinPEAS**

* Script que automatiza la enumeración del sistema para encontrar vectores de escalación.
* Ejecución:

  ```cmd
  C:\> winpeas.exe > outputfile.txt
  ```
* Descarga: [WinPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/winPEAS)

**2. PrivescCheck**

* PowerShell script para buscar vectores comunes de escalación.
* Puede requerir bypass de la política de ejecución:

  ```powershell
  PS C:\> Set-ExecutionPolicy Bypass -Scope process -Force
  PS C:\> . .\PrivescCheck.ps1
  PS C:\> Invoke-PrivescCheck
  ```
* Descarga: [PrivescCheck](https://github.com/itm4n/PrivescCheck)

**3. WES-NG (Windows Exploit Suggester - Next Generation)**

* Python script que analiza parches faltantes del sistema a partir de `systeminfo`.
* Flujo:

  1. Exportar `systeminfo` del objetivo:

     ```cmd
     systeminfo > systeminfo.txt
     ```
  2. Transferir a la máquina atacante (Kali/TryHackMe).
  3. Ejecutar:

     ```bash
     wes.py systeminfo.txt
     ```
* Actualizar base de datos antes de usar:

  ```bash
  wes.py --update
  ```

**4. Metasploit – Local Exploit Suggester**

* Requiere Meterpreter shell en el objetivo.
* Módulo: `multi/recon/local_exploit_suggester`
* Lista vulnerabilidades locales que permiten escalar privilegios.

**Notas clave:**

* Automatización acelera la enumeración, pero puede omitir vectores.
* WinPEAS y scripts similares deben ejecutarse en el objetivo; WES-NG permite análisis desde la máquina atacante, reduciendo ruido.
* Siempre revisar resultados manualmente y confirmar posibles vulnerabilidades antes de explotar.

---

###  Recursos Avanzados de Escalación de Privilegios en Windows

**Frente:**
¿Qué recursos permiten profundizar en técnicas de escalación de privilegios en Windows?

**Reverso:**
**1. Guías y repositorios:**

* **PayloadsAllTheThings – Windows Privilege Escalation**: colección de exploits y técnicas para elevar privilegios.
* **Priv2Admin**: abuso de privilegios de Windows para escalar a administrador.
* **RogueWinRM Exploit**: explotación de Windows Remote Management mal configurado.
* **Potatoes**: técnicas de escalación basadas en token impersonation y bypass de UAC.
* **Decoder's Blog**: blog con tutoriales y análisis de vectores de escalación.
* **Token Kidnapping**: técnicas avanzadas de secuestro de tokens para elevar privilegios.
* **Hacktricks – Windows Local Privilege Escalation**: recopilación de métodos prácticos para escalación local.

**Claves de estudio:**

* Estos recursos amplían lo visto en enumeración, software vulnerable y exploits locales.
* Permiten estudiar técnicas desde básicas hasta avanzadas, incluyendo abuso de tokens y servicios mal configurados.
* Útiles para práctica en laboratorios y red teaming.
