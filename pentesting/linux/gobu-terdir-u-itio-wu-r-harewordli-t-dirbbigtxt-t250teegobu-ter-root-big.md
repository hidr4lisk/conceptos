# gobuster dir -u SITIO -w /usr/share/wordlists/dirb/big.txt -t 250 | tee gobuster-root-big

## -x EXTENSION para archivos

Componentes

gobuster: herramienta para fuzzing de directorios/archivos, DNS, etc.

dir: modo de enumeración de directorios/archivos en un sitio web.

-u SITIO: URL objetivo. Ejemplo: http://10.10.10.10/.

-w /usr/share/wordlists/dirb/big.txt: wordlist a usar para probar nombres de directorios/archivos. En este caso, big.txt de dirb.

-t 250: número de hilos concurrentes. Aquí son 250 threads lanzados al mismo tiempo (muy agresivo, rápido pero puede saturar servidor o perder respuestas).

| tee gobuster-root-big: redirige la salida estándar del comando a dos sitios:

la terminal (pantalla)

el archivo gobuster-root-big (se crea o sobreescribe con el output).