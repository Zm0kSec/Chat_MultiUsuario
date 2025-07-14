# AnonChat_Terminal: Chat Multiusuario Seguro (SSL) con Estilo Hacker

![AnonChat Screenshot](https://raw.githubusercontent.com/Zm0kSec/Chat_MultiUsuario/main/docs/image.png)


Bienvenido a `AnonChat_Terminal`, un sistema de chat multiusuario seguro y de código abierto desarrollado en Python. Este proyecto utiliza cifrado SSL/TLS para proteger tus comunicaciones y presenta una interfaz de usuario minimalista con una estética inspirada en terminales y el "modo hacker", gracias a la magia de [CustomTkinter](https://customtkinter.tomschimansky.com/).

**Características Clave:**

* **Comunicación Cifrada (SSL/TLS):** Tus mensajes viajan de forma segura entre clientes y el servidor.
* **Chat Multiusuario:** Conéctate y chatea en tiempo real con múltiples usuarios.
* **Notificaciones por Correo Electrónico:** Envía alertas a usuarios específicos o a todos los participantes que hayan registrado su correo.
* **Detección de Usuarios Duplicados:** Evita que varios usuarios se conecten con el mismo nombre.
* **Interfaz de Usuario "Hacksor":** Una estética oscura, con texto verde neón y elementos de terminal para una experiencia visual única.

---

## 🚀 Guía de Inicio Rápido

Sigue estos pasos para poner en marcha tu `AnonChat_Terminal`. ¡No necesitas ser un experto para hacerlo funcionar!

### 1. Requisitos del Sistema

Asegúrate de tener lo siguiente instalado en tu PC:

* **Python 3.x:** Puedes descargarlo desde [python.org/downloads/](https://www.python.org/downloads/).
* **Git:** Para clonar este repositorio. Descárgalo desde [git-scm.com/downloads](https://git-scm.com/downloads).
* **OpenSSL:** Necesario para generar los certificados de seguridad. Generalmente viene preinstalado en Linux y macOS. En Windows, suele incluirse con [Git Bash](https://git-scm.com/downloads) o puedes instalarlo por separado.

### 2. Preparación del Entorno

#### a) Clonar el Repositorio

Abre tu terminal (PowerShell en Windows, Terminal en macOS/Linux) y ejecuta:

```bash
git clone [https://github.com/tu_usuario/tu_repositorio.git](https://github.com/tu_usuario/tu_repositorio.git)
cd tu_repositorio
(¡Importante! Reemplaza https://github.com/tu_usuario/tu_repositorio.git con la URL real de tu repositorio de GitHub.)

b) Instalar Dependencias de Python
Desde la misma carpeta del proyecto en tu terminal, instala la librería CustomTkinter:

Bash

pip install customtkinter
Las demás librerías (socket, threading, ssl, re, smtplib, email, tkinter) son estándar en Python y ya deberían estar instaladas.

c) Generar Certificados de Seguridad (SSL)
Este chat usa SSL/TLS para una comunicación segura. Necesitas generar dos archivos clave: un certificado (.pem) y una clave privada (.key).

Desde la carpeta del proyecto en tu terminal, ejecuta este comando:

Bash

openssl req -x509 -newkey rsa:2048 -keyout server-key.key -out server-cert.pem -days 365 -nodes
¿Qué hace este comando? Genera un certificado autofirmado (server-cert.pem) y una clave privada (server-key.key) válidos por 365 días. La opción -nodes significa "no des-encriptar", lo cual es conveniente para este ejemplo porque no te pedirá una contraseña cada vez que inicies el servidor.

Durante el proceso: openssl te hará varias preguntas (país, estado, ciudad, organización, etc.). Puedes dejar la mayoría en blanco si lo deseas, excepto por "Common Name (e.g. server FQDN or YOUR name)", donde puedes escribir localhost o cualquier nombre que quieras.

d) Configurar el Envío de Correos Electrónicos (Solo para el Servidor)
El servidor tiene la capacidad de enviar notificaciones por correo electrónico (actualmente configurado para Gmail). Para que funcione, necesitas una contraseña de aplicación para tu cuenta de Gmail, ya que las contraseñas normales ya no son compatibles para inicios de sesión de terceros.

Genera una Contraseña de Aplicación para Gmail:

Ve a la configuración de seguridad de tu cuenta de Google.

Busca la sección "Cómo inicias sesión en Google".

Haz clic en "Contraseñas de aplicaciones" (si no la ves, activa la verificación en dos pasos primero).

Sigue las instrucciones para generar una nueva contraseña de aplicación (será una cadena de 16 caracteres). Copia esta contraseña.

Actualiza el Código del Servidor:

Abre el archivo Server_Chat_finish.py en un editor de texto.

Busca las líneas:

Python

EMAIL_SERVER = "email de servidor a usar"
EMAIL_PASS = "clave de aplicacion"
Reemplaza "email de servidor a usar" con tu dirección de correo electrónico de Gmail.

Reemplaza "clave de aplicacion" con la contraseña de aplicación de 16 caracteres que generaste.

3. Ejecutar el Chat
Ahora que todo está configurado, puedes iniciar el servidor y los clientes.

a) Iniciar el Servidor
Abre una terminal nueva, navega a la carpeta de tu proyecto (cd tu_repositorio) y ejecuta:

Bash

python Server_Chat_finish.py
Verás el mensaje "Waiting for connection". Deja esta terminal abierta y en ejecución.

b) Iniciar los Clientes
Abre una o más terminales nuevas (cada terminal será un usuario diferente), navega a la carpeta de tu proyecto (cd tu_repositorio) y ejecuta en cada una:

Bash

python Client_chat_finish.py
Paso a paso del Cliente:

Te pedirá un nombre de usuario. Ingrésalo (ej. zmk, froat, sudo).

El sistema verificará si el nombre está en uso. Si lo está, te lo indicará y el cliente se cerrará para que elijas otro.

Luego, te preguntará si deseas notificaciones por correo electrónico (si o no).

Si eliges si, te pedirá tu dirección de correo. Ingrésala correctamente para recibir notificaciones.

Si eliges no, entrarás en "modo incógnito" sin notificaciones por correo.

Una vez conectado, aparecerá la ventana de chat con la estética "hacksor".

4. Uso del Chat
Enviar Mensajes Generales:

Escribe tu mensaje en el campo de texto inferior (donde dice // Connected as <tu_usuario> //).

Presiona el botón "SEND_MSG" o la tecla Enter.

Tu mensaje se enviará a todos los usuarios conectados y aparecerá en verde neón en tu chat.

Enviar Notificaciones por Correo:

En el campo de texto de notificación (donde dice // Target User or GENERAL for Notification //), puedes hacer dos cosas:

Notificar a un Usuario Específico: Escribe el nombre de usuario exacto de la persona a la que quieres enviar una notificación (solo funcionará si esa persona ingresó su correo al conectarse y tu servidor está bien configurado).

Notificar a Todos (General): Escribe GENERAL (en mayúsculas o minúsculas, el sistema lo interpretará igual).

Después de escribir el objetivo, presiona el botón "NOTIFY_USER" o Ctrl + e.

Verás un mensaje en el chat confirmando el intento de notificación.

Salir del Chat:

Puedes simplemente cerrar la ventana del chat.

O bien, en la terminal donde se está ejecutando el cliente, presiona Ctrl + c.

💡 Consejos y Trucos Adicionales
Nombres de Usuario: Intenta usar nombres de usuario únicos y significativos para evitar confusiones.

Certificados SSL: Los certificados generados son autofirmados y solo válidos por un año (-days 365). Para un entorno de producción o más serio, necesitarías certificados emitidos por una Autoridad de Certificación (CA).

Seguridad de Credenciales: La contraseña de aplicación de Gmail está directamente en el código del servidor. Para proyectos reales, considera usar variables de entorno o un sistema de gestión de secretos para mantener estas credenciales seguras.

Personalización del Estilo: Abre Client_chat_finish.py y experimenta con las constantes al principio del archivo (THEME_COLOR_PRIMARY, THEME_COLOR_SECONDARY, FONT_FAMILY, etc.) para cambiar la apariencia del chat a tu gusto.

Resolución de Problemas:

Si el cliente no se conecta, asegúrate de que el servidor esté en ejecución y que no haya errores en su terminal.

Si los certificados dan problemas, intenta regenerarlos con el comando openssl y asegúrate de que estén en la misma carpeta que Server_Chat_finish.py.

Si los correos no se envían, verifica tu contraseña de aplicación de Gmail y asegúrate de que tu cuenta tenga la verificación en dos pasos activada.

📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta la sección a continuación para más detalles sobre cómo aplicar y entender esta licencia.
