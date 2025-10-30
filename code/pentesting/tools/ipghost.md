**Flashcard IPGhost**

* **Qué es:** Herramienta CLI que rota automáticamente la IP pública usando la red Tor.
* **Función principal:** Cambiar periódicamente la IP de salida sin intervención manual.
* **Cómo funciona:** Crea y renueva circuitos Tor para obtener nuevas IPs de salida.
* **Requisitos:** Tor instalado y configurado (proxy SOCKS5 127.0.0.1:9050).
* **Usos:** Anonimato parcial, evasión de bloqueos, distribución de peticiones en pentesting y OSINT.
* **Limitaciones:** Menor velocidad que VPN, bloqueo por servicios contra Tor, no protege datos fuera del tráfico Tor.
* **Instalación básica:**

  ```
  git clone https://github.com/s-r-e-r-a-j/IPGhost.git
  cd IPGhost
  sudo bash install.sh
  sudo ipghost
  ```
* **Configuración:** Define intervalo de cambio y cantidad de ciclos.
* **Resultado:** IP y ubicación nueva tras cada ciclo; detiene Tor al salir.
