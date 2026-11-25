
"""
twichionBOT - Open Source Twitch AI Bot
Copyright (c) twichionBOT contributors

Configuration is provided through environment variables.
Never put API keys or Twitch tokens directly in this file.
"""

import os
import re
import time
import socket
import threading
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from groq import Groq


# =========================================================
# CONFIGURATION
# =========================================================

BOT_NAME = os.getenv("BOT_NAME", "twichionBOT").strip()
BOT_NICK = os.getenv("TWITCH_BOT_NICK", "twichionbot").strip().lower()

TWITCH_TOKEN = os.getenv("TWITCH_TOKEN", "").strip()
TWITCH_CHANNELS = [
    channel.strip().lstrip("#").lower()
    for channel in os.getenv("TWITCH_CHANNELS", "").split(",")
    if channel.strip()
]

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b").strip()

BOT_PREFIX = os.getenv("BOT_PREFIX", "!ask").strip()

SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are a friendly and helpful Twitch chat assistant. "
    "Answer briefly, clearly, and in the language used by the viewer."
)

PORT = int(os.getenv("PORT", "10000"))

IRC_HOST = "irc.chat.twitch.tv"
IRC_PORT = 6667

MAX_MESSAGE_LENGTH = 450
REQUEST_COOLDOWN = 3

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s"
)

logger = logging.getLogger("twichionBOT")


# =========================================================
# AI ENGINE
# =========================================================

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def ask_ai(prompt):
    if not groq_client:
        return "La IA no está configurada. Contacta al administrador."

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=250,
            temperature=0.7
        )

        answer = response.choices[0].message.content or ""
        answer = re.sub(r"\s+", " ", answer).strip()

        return answer[:MAX_MESSAGE_LENGTH] or "No pude generar una respuesta."

    except Exception:
        logger.exception("Error al consultar Groq")
        return "La IA tuvo un problema al responder."


# =========================================================
# TWITCH IRC
# =========================================================

class TwitchBot:

    def __init__(self):
        self.connection = None
        self.running = True
        self.last_request = {}

    def send_message(self, channel, message):
        if not self.connection:
            return

        message = re.sub(r"[\r\n]+", " ", message).strip()
        message = message[:MAX_MESSAGE_LENGTH]

        if not message:
            return

        payload = f"PRIVMSG #{channel} :{message}\r\n"

        try:
            self.connection.send(payload.encode("utf-8"))
        except OSError:
            logger.warning("No se pudo enviar el mensaje a #%s", channel)

    def connect(self):
        if not TWITCH_TOKEN or not TWITCH_CHANNELS:
            logger.error(
                "Configura TWITCH_TOKEN y TWITCH_CHANNELS para activar Twitch."
            )
            return False

        try:
            self.connection = socket.socket()
            self.connection.settimeout(1)
            self.connection.connect((IRC_HOST, IRC_PORT))

            self.connection.send(
                f"PASS {TWITCH_TOKEN}\r\n".encode("utf-8")
            )
            self.connection.send(
                f"NICK {BOT_NICK}\r\n".encode("utf-8")
            )
            self.connection.send(
                b"CAP REQ :twitch.tv/tags twitch.tv/commands\r\n"
            )

            for channel in TWITCH_CHANNELS:
                self.connection.send(
                    f"JOIN #{channel}\r\n".encode("utf-8")
                )

            logger.info("Conectado a Twitch IRC.")
            return True

        except OSError:
            logger.exception("No se pudo conectar a Twitch.")
            self.disconnect()
            return False

    def disconnect(self):
        if self.connection:
            try:
                self.connection.close()
            except OSError:
                pass

        self.connection = None

    def handle_message(self, raw):
        if raw.startswith("PING"):
            self.connection.send(b"PONG :tmi.twitch.tv\r\n")
            return

        if " PRIVMSG " not in raw:
            return

        try:
            prefix, content = raw.split(" PRIVMSG ", 1)
            channel, message = content.split(" :", 1)

            channel = channel.lstrip("#").lower()
            username = prefix.split("!", 1)[0].lstrip(":")

            if username.lower() == BOT_NICK:
                return

            if not message.lower().startswith(BOT_PREFIX.lower() + " "):
                return

            prompt = message[len(BOT_PREFIX):].strip()

            if not prompt:
                self.send_message(
                    channel,
                    f"Usa {BOT_PREFIX} seguido de tu pregunta."
                )
                return

            now = time.time()
            previous = self.last_request.get(channel, 0)

            if now - previous < REQUEST_COOLDOWN:
                return

            self.last_request[channel] = now

            logger.info(
                "Pregunta recibida en #%s de %s",
                channel,
                username
            )

            answer = ask_ai(prompt)
            self.send_message(channel, f"@{username} {answer}")

        except (ValueError, IndexError):
            logger.warning("Mensaje IRC no reconocido.")

    def run(self):
        while self.running:
            if not self.connection:
                if not self.connect():
                    time.sleep(10)
                    continue

            try:
                data = self.connection.recv(4096)

                if not data:
                    raise ConnectionError("Twitch cerró la conexión")

                for line in data.decode(
                    "utf-8", errors="ignore"
                ).split("\r\n"):
                    if line:
                        self.handle_message(line)

            except socket.timeout:
                continue

            except (OSError, ConnectionError):
                logger.warning("Conexión Twitch perdida. Reconectando...")
                self.disconnect()
                time.sleep(5)


# =========================================================
# WEB SERVER FOR RENDER
# =========================================================

class SimpleHandler(BaseHTTPRequestHandler):

    def respond(self, content, content_type):
        encoded = content.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

        if self.command != "HEAD":
            self.wfile.write(encoded)

    def do_HEAD(self):
        self.respond("", "text/plain; charset=utf-8")

    def do_GET(self):

        if self.path == "/health":
            return self.respond(
                '{"status":"online","bot":"twichionBOT"}',
                "application/json; charset=utf-8"
            )

        channels_html = (
            ", ".join(f"#{channel}" for channel in TWITCH_CHANNELS)
            or "No configurados"
        )

        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{BOT_NAME} - Status</title>
            <style>
                body {{
                    background: #0f172a;
                    color: #e2e8f0;
                    font-family: monospace;
                    text-align: center;
                    padding: 50px 15px;
                }}
                .card {{
                    background: #1e293b;
                    border: 2px solid #a855f7;
                    display: inline-block;
                    padding: 30px;
                    border-radius: 12px;
                    max-width: 500px;
                }}
                h1 {{ color: #c084fc; }}
                .online {{ color: #4ade80; }}
                .muted {{ color: #94a3b8; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🤖 {BOT_NAME}</h1>
                <p class="online">● WEB SERVER ONLINE</p>
                <p>Twitch channels: {channels_html}</p>
                <p>AI model: {GROQ_MODEL}</p>
                <p class="muted">Open Source Twitch AI Bot</p>
                <p class="muted">Powered by Render + Groq</p>
            </div>
        </body>
        </html>
        """

        self.respond(html, "text/html; charset=utf-8")

    def log_message(self, format, *args):
        logger.info("HTTP: " + format, *args)


def start_web_server():
    server = ThreadingHTTPServer(
        ("0.0.0.0", PORT),
        SimpleHandler
    )

    logger.info("Web server listening on port %s", PORT)
    server.serve_forever()


# =========================================================
# START APPLICATION
# =========================================================

def main():
    logger.info("Starting %s...", BOT_NAME)

    web_thread = threading.Thread(
        target=start_web_server,
        daemon=True
    )
    web_thread.start()

    if not GROQ_API_KEY:
        logger.warning("GROQ_API_KEY no configurada. La IA no responderá.")

    bot = TwitchBot()

    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("Apagando bot...")
    finally:
        bot.running = False
        bot.disconnect()


if __name__ == "__main__":
    main()
