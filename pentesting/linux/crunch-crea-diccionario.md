**Flashcard – Crunch (generación de diccionarios con patrón y rango)**

**Pregunta:**
¿Qué genera el comando

```bash
crunch 3 3 -o otp.txt -t %%% -s 100 -e 200
```

y qué significa cada flag?

**Respuesta:**

* `3 3` → cadenas de longitud exacta 3.
* `-o otp.txt` → guarda en `otp.txt`.
* `-t %%%` → patrón de 3 dígitos (`%` = número 0–9).
* `-s 100` → empieza en 100.
* `-e 200` → termina en 200.
* Resultado: un diccionario con los números del 100 al 200.

¿Querés que te arme más flashcards de **crunch** con otros patrones (`@`, `,`, `^`) para cubrir letras y símbolos?
