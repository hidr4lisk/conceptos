### El error ocurre porque las claves GPG que validan las firmas criptográficas del repositorio fueron rotadas (cambiadas) y tu sistema no tiene la nueva clave pública.

## Cómo prevenir el problema

Ejecutar periódicamente:

    sudo apt-key list

Seguir el blog oficial de la distribución o revisar:

    https://www.kali.org/news/

Automatizar importación de claves con scripts o herramientas como ansible en despliegues.