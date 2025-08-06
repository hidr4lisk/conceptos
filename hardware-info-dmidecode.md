Fabricante	

    sudo dmidecode -s system-manufacturer
    
Nombre del producto (modelo)	

    sudo dmidecode -s system-product-name

Versión del sistema	

    sudo dmidecode -s system-version

Número de serie	

    sudo dmidecode -s system-serial-number

Todo el resumen del sistema	

    sudo dmidecode -t system



para agregar a la lista /etc/hosts

    echo "IP SITIO" | sudo tee -a /etc/hosts > /dev/null

Explicación mínima:

    echo: genera la línea.

    | sudo tee -a: eleva privilegios y agrega al archivo (-a = append).

    > /dev/null: oculta la salida estándar de tee.    