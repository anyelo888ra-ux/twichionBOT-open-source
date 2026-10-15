# 🤖 twichionBOT v3.0 (Dual Core)

**twichionBOT** es un bot de streaming multi-plataforma diseñado para conectarse simultáneamente a los chats de **Twitch** y **Kick**, impulsado con Inteligencia Artificial (**Groq AI**) y equipado con un servidor web ligero para mantenerse activo 24/7 en plataformas de la nube como **Render**.

---

## 🚀 Características

- **Multi-Streaming Simultáneo**: Conexión paralela mediante sockets y WebSockets para Twitch y Kick.
- **Inteligencia Artificial integrada**: Utiliza la API de Groq para responder de forma inteligente a las menciones del chat.
- **Servidor Web Incorporado**: Incluye un panel visual de estado (`ONLINE & MULTI-CONECTADO`) ideal para despliegues en la nube.
- **Preparado para Open Source**: Código modular totalmente desacoplado de credenciales personales mediante variables de entorno.

---

## ⚙️ Requisitos previos

1. Python 3.9 o superior instalado.
2. Una cuenta en [Groq Console](https://console.groq.com/) para obtener tu `GROQ_API_KEY`.
3. Un token de OAuth de Twitch para tu cuenta de bot.
4. Una cookie de sesión (`kick_session`) si deseas conectarlo a Kick.

---

## 🛠️ Instalación y Configuración Local

### 1. Clonar el repositorio
```bash
git clone [https://github.com/anyelo888ra-ux/twichionBOT-open-source.git](https://github.com/anyelo888ra-ux/twichionBOT-open-source.git)
cd twichionBOT-open-source

```

### 2. Instalar dependencias

Crea un archivo `requirements.txt` con el siguiente contenido:

```text
requests==2.31.0
aiohttp==3.9.3
websockets==12.0
curl_cffi>=0.7.0
kickpython==0.1.5

```

Y luego instálalas ejecutando:

```bash
pip install -r requirements.txt

```

---

## ☁️ Despliegue en la Nube (Ej: Render)

1. Sube este repositorio a tu cuenta de GitHub de forma pública.
2. En [Render.com](https://render.com/), crea un nuevo **Web Service** y conéctalo a este repositorio.
3. Configura el **Start Command**:
```bash
python main.py

```


4. Añade todas las variables de entorno detalladas en la sección anterior dentro de la pestaña **Environment** en Render.
5. ¡Listo! El bot levantará el servidor web y se conectará automáticamente a los chats.

---

## 📜 Licencia

Este proyecto se distribuye bajo los términos de la licencia MIT. ¡Siéntete libre de clonarlo, mejorarlo y adaptarlo a tus directos!
