reverse-shell-generator es una herramienta web (https://revshells.com) que automatiza la creación de comandos de reverse shell y listeners en múltiples lenguajes y formatos. Su utilidad es práctica en CTFs o pentesting cuando necesitas generar rápidamente un payload válido para una víctima y su correspondiente comando de escucha en el atacante.

FUNCIONALIDADES PRINCIPALES

    Generar shells y listeners comunes
    Produce comandos listos para copiar en Bash, Python, PHP, PowerShell, Perl, etc., tanto para reverse como para bind shells.

    Guardar payloads
    Permite descargar directamente el payload generado como archivo desde el navegador.

    Raw mode + curl
    Modo “raw” devuelve el payload en texto puro, lo que permite enviarlo directamente con curl a otro sistema para guardarlo o ejecutarlo.

    Incremento automático de puerto
    Botón que aumenta el puerto por 1 para agilizar pruebas cuando un puerto está ocupado.

    Codificación
    Puede codificar el payload en URI encoding o Base64 para evadir filtros o WAFs.

    Persistencia
    Usa localStorage del navegador para mantener la configuración (IP, puerto, preferencias).

    Modos visuales
    Dark, Light y Meme Mode (estético, no funcional).

    Integración con HoaxShell
    Permite generar payloads compatibles con el framework HoaxShell y su listener.