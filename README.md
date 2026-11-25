# 🤖 twichionBOT — Open Source AI Streaming Bot

**twichionBOT** es un bot de streaming impulsado por Inteligencia Artificial, diseñado para ayudar a creadores de contenido a interactuar con sus comunidades en Twitch.

Utiliza **Groq AI** para generar respuestas inteligentes en tiempo real y cuenta con un servidor web ligero para facilitar su despliegue en servicios como Render.

El proyecto es Open Source: cualquier persona puede utilizarlo, modificarlo y contribuir a su desarrollo.

---

## 🚀 Características

- **Integración con Twitch:** conexión al chat mediante Twitch IRC.
- **Inteligencia Artificial:** respuestas generadas mediante la API de Groq.
- **Modelo configurable:** permite seleccionar el modelo de IA mediante variables de entorno.
- **Comandos personalizados:** utiliza `!ask` para consultar a la IA desde el chat.
- **Servidor web integrado:** página de estado y endpoint `/health`.
- **Compatible con Render:** preparado para ejecutarse como Web Service.
- **Configuración independiente:** cada usuario utiliza sus propios tokens y credenciales.
- **Open Source:** permite crear modificaciones y contribuir al proyecto.

### 🔮 Próximamente

- Integración estable con Kick.
- Panel web para administrar el bot.
- Más comandos personalizados.
- Configuración de personalidad de la IA.
- Nuevas integraciones y plataformas.

---

## ⚙️ Requisitos

Antes de comenzar necesitas:

1. Python 3.9 o superior.
2. Una cuenta en [Groq Console](https://console.groq.com/) para obtener una API Key.
3. Una cuenta de Twitch para crear y configurar tu bot.
4. Un token OAuth válido para conectarte al chat de Twitch.

---

## 🛠️ Instalación local

### 1. Clonar el repositorio

```bash
git clone https://github.com/anyelo888ra-ux/twichionBOT-open-source.git
cd twichionBOT-open-source
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crea un archivo llamado `.env` tomando como referencia `.env.example`.

Configura tus propios valores:

```env
BOT_NAME=twichionBOT
TWITCH_BOT_NICK=twichionbot

TWITCH_TOKEN=oauth:YOUR_TWITCH_TOKEN
TWITCH_CHANNELS=your_channel

GROQ_API_KEY=YOUR_GROQ_API_KEY
GROQ_MODEL=openai/gpt-oss-20b

BOT_PREFIX=!ask
PORT=10000
```

No compartas tu archivo `.env` ni publiques tus tokens en GitHub.

**Importante:** el código actual utiliza variables de entorno. Para cargar automáticamente el archivo `.env` en local, instala `python-dotenv` y añade `load_dotenv()` al inicio de `main.py`. En Render puedes configurar las variables directamente desde el panel de Environment.

### 4. Ejecutar el bot

```bash
python main.py
```

¡Listo! El bot iniciará el servidor web e intentará conectarse a Twitch.

---

## 💬 Uso en Twitch

Una vez conectado, escribe en el chat:

```text
!ask ¿Qué es la inteligencia artificial?
```

El bot responderá utilizando el modelo de Groq configurado.

Puedes cambiar el prefijo mediante `BOT_PREFIX`.

---

## ☁️ Despliegue en Render

1. Sube o haz Fork del repositorio en GitHub.
2. Entra en [Render](https://render.com/).
3. Crea un nuevo **Web Service**.
4. Conecta tu repositorio.
5. Configura los siguientes comandos:

**Build Command**

```bash
pip install -r requirements.txt
```

**Start Command**

```bash
python main.py
```

6. En la sección **Environment**, añade las variables de entorno necesarias:
   - `BOT_NAME`
   - `TWITCH_BOT_NICK`
   - `TWITCH_TOKEN`
   - `TWITCH_CHANNELS`
   - `GROQ_API_KEY`
   - `GROQ_MODEL`
   - `BOT_PREFIX`

7. Despliega el servicio.

El servidor web estará disponible en la URL que Render proporcione.

### Comprobar el estado

Página principal:

```text
https://TU-SERVICIO.onrender.com/
```

Endpoint de salud:

```text
https://TU-SERVICIO.onrender.com/health
```

**Nota:** `/health` comprueba que el servidor HTTP responde. No garantiza que Twitch o Groq estén conectados correctamente.

---

## 🤝 Contribuir al proyecto

¡Las contribuciones son bienvenidas!

Puedes ayudar de diferentes maneras:

- Encontrando y reportando errores.
- Mejorando el código Python.
- Añadiendo comandos nuevos.
- Integrando otras plataformas.
- Mejorando la documentación.
- Optimizando el rendimiento.
- Proponiendo nuevas características.

### Cómo colaborar

1. Haz Fork del repositorio.
2. Crea una rama para tus cambios.
3. Realiza tus modificaciones.
4. Prueba el código.
5. Envía un Pull Request.

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para conocer las pautas de colaboración.

---

## 📁 Estructura del proyecto

```text
twichionBOT/
├── main.py
├── README.md
├── LICENSE
├── requirements.txt
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── .github/
    ├── ISSUE_TEMPLATE/
    └── PULL_REQUEST_TEMPLATE.md
```

---

## 🔐 Seguridad

- Nunca publiques tus API Keys.
- No compartas tokens OAuth.
- No subas archivos `.env`.
- Utiliza tus propias credenciales.
- Reporta vulnerabilidades sin publicar información sensible.

---

## 📜 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

Consulta el archivo [LICENSE](LICENSE) para conocer sus términos.

Puedes utilizar, modificar y distribuir el proyecto respetando las condiciones de la licencia.

---

## 💜 Créditos

**twichionBOT Open Source**

Desarrollado para creadores de contenido y comunidades de streaming.

- [GitHub Repository](https://github.com/anyelo888ra-ux/twichionBOT-open-source)
- [Groq](https://groq.com/)
- [Twitch](https://www.twitch.tv/)

¡Gracias a todas las personas que ayudan a mejorar twichionBOT! 🚀
