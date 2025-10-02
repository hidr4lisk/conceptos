# https://tryhackme.com/room/oauthvulnerabilities

---

### ✅ **Traducción al español**

El flujo de OAuth 2.0 comienza cuando un usuario (Propietario del recurso) interactúa con una aplicación cliente (Cliente) y solicita acceso a un recurso específico. El cliente redirige al usuario a un servidor de autorización, donde se le solicita que inicie sesión y otorgue acceso. Si el usuario da su consentimiento, el servidor de autorización emite un código de autorización, que el cliente puede intercambiar por un token de acceso. Este token permite al cliente acceder al servidor de recursos y recuperar el recurso solicitado en nombre del usuario.

#### Proceso de flujo OAuth reflejando todos los pasos

Discutiremos en detalle varios pasos del flujo de trabajo de OAuth, considerando el mismo ejemplo de CoffeeShopApp.

#### Conectarse a la Máquina

Puedes iniciar la máquina virtual haciendo clic en el botón "Start Machine" adjunto a esta tarea para abrir la VM en pantalla dividida. Por favor, espera 1-2 minutos después de que el sistema haya arrancado completamente para permitir que los scripts automáticos se ejecuten con éxito.

Usaremos una versión personalizada del kit de herramientas OAuth de Django como proveedor OAuth. Es muy importante entender que cuando se use el término proveedor OAuth en las próximas tareas, se refiere al proveedor de terceros con el que queremos integrarnos/autenticarnos. Por ejemplo, en el caso de "Iniciar sesión con FactBook", FactBook es el proveedor OAuth. Además, en estas tareas, el proveedor OAuth, es decir, CoffeeShopApp, permanecerá igual; sin embargo, los clientes (la aplicación que queremos integrar) cambiarán en cada tarea.

Puedes visitar la URL [http://coffee.thm:8000/admin](http://coffee.thm:8000/admin) para ver el panel de inicio de sesión del proveedor OAuth, el cual será el mismo durante todo el laboratorio.

---

### ✴️ **Resumen breve**

El flujo OAuth 2.0 permite a un usuario autorizar a una aplicación para acceder a sus datos sin compartir su contraseña. En este caso, se utiliza una app llamada **CoffeeShopApp** como proveedor OAuth. Se usará una VM con una versión personalizada del sistema OAuth de Django para realizar prácticas de integración. Aunque el proveedor será siempre el mismo, las aplicaciones cliente cambiarán en cada ejercicio.

---

### 💡 **Explicación breve**

OAuth 2.0 es un protocolo de autorización que permite a una app acceder a recursos protegidos en nombre de un usuario. El proceso implica que el usuario otorga permiso a través de un servidor de autorización, el cual genera un **código de autorización** que luego la app cambia por un **token de acceso**. Ese token le da acceso a los datos del usuario sin exponer sus credenciales.

---

### 📘 **Glosario**

| Término                              | Significado                                                                   |
| ------------------------------------ | ----------------------------------------------------------------------------- |
| **OAuth 2.0**                        | Protocolo para autorización segura entre aplicaciones.                        |
| **Usuario (Resource Owner)**         | Persona que posee los datos o recursos protegidos.                            |
| **Cliente (Client)**                 | Aplicación que quiere acceder a los datos del usuario.                        |
| **Proveedor OAuth (OAuth Provider)** | Servicio que autentica al usuario y emite tokens (ej: Google, CoffeeShopApp). |
| **Servidor de autorización**         | Componente que autentica al usuario y entrega el código de autorización.      |
| **Código de autorización**           | Código temporal que el cliente intercambia por un token de acceso.            |
| **Token de acceso**                  | Token que permite al cliente acceder a recursos protegidos.                   |
| **Servidor de recursos**             | Servidor que contiene los datos protegidos del usuario.                       |
| **VM (Máquina Virtual)**             | Entorno simulado donde se realizan las prácticas.                             |

---
