import os
import socket
import requests
import threading
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
# Importación correcta de la librería kickpython
from kickpython import KickAPI

# === CONFIGURACIÓN GENERAL ===
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', 'gsk_123456789wty015-ejemplo-quita-esto-y-pon-tu-api-key-para-la-ia')
# Endpoint oficial unificado para Groq
GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'

# --- CONFIGURACIÓN TWITCH ---
SERVER_TWITCH = 'irc.chat.twitch.tv'
PORT_TWITCH = 6667
TOKEN_TWITCH = os.environ.get('TWITCH_TOKEN', 'oauth:123456789wty015-ejemplo-quita-esto-y-pon-tu-oauth-de-tu-cuenta-del-bot')
NICKNAME_TWITCH = 'twichionbot'
# Canales en formato lista/tupla para conectar
CHANNELS_TWITCH = ['#c00lkidd_v2ytofficial', '#twichionbot']

# --- CONFIGURACIÓN KICK ---
# Si en Render pones KICK_STREAMER = c00lkidd-v2yt,twichionbot
KICK_STREAMER_RAW = os.environ.get('KICK_STREAMERS', 'c00lkidd-v2yt')
KICK_STREAMERS = [s.strip() for s in KICK_STREAMER_RAW.split(',')]
KICK_TOKEN = os.environ.get('KICK_TOKEN', os.environ.get('kick_session', '123456789wty015-ejemplo-quita-esto-y-pon-tu-kick-session-de-tu-cuenta-del-bot'))
KICK_CLIENT_ID = os.environ.get('KICK_CLIENT_ID', 'esto-puede-ser-incesario-asique-no-importa')  

# --- SERVIDOR WEB PARA RENDER ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>twichionBOT Multi-Stream Status</title>
            <style>
                body {{ background: #0f172a; color: #38bdf8; font-family: monospace; text-align: center; padding-top: 50px; }}
                .card {{ background: #1e293b; border: 2px solid #a855f7; display: inline-block; padding: 30px; border-radius: 12px; box-shadow: 0 0 20px rgba(168, 85, 247, 0.2); }}
                h1 {{ margin-top: 0; color: #f43f5e; }}
                .status {{ color: #4ade80; font-weight: bold; }}
                .platform {{ margin: 10px 0; font-size: 16px; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🤖 twichionBOT v3.0 (Dual Core)</h1>
                <p>Estado del sistema: <span class="status">ONLINE &amp; MULTI-CONECTADO</span></p>
                <div class="platform">💜 Twitch: <b>{', '.join(CHANNELS_TWITCH)}</b></div>
                <<div class="platform">💚 Kick: <b>#{', '.join(KICK_STREAMERS)}</b></div>
                <p style="font-size: 12px; color: #94a3b8; margin-top: 20px;">Corriendo en paralelo en la nube de Render 🚀</p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

def iniciar_servidor_web():
    port_web = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port_web), SimpleHandler)
    print(f"[Web] Servidor de estado corriendo en el puerto {port_web}")
    server.serve_forever()

# --- LÓGICA UNIFICADA DE IA (GROQ) ---
def consultar_ia_groq(prompt_usuario, autor, plataforma):
    if not GROQ_API_KEY:
        return "¡Ey! Falta configurar la API key de Groq, crack."
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "lama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": f"Eres twichionBOT, un bot amigable que asiste en {plataforma}. Responde en español, de forma muy concisa y directa (máximo 1 o 2 oraciones)."
            },
            {
                "role": "user",
                "content": f"{autor} dice: {prompt_usuario}"
            }
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(GROQ_URL, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content'].strip().replace('\n', ' ')
        else:
            # Esto imprimirá el error exacto en tu consola de Render o VS Code si vuelve a fallar
            print(f"[Groq Error Detalle]: {response.text}")
            return f"¡Vaya! Groq rechazó la petición (Código {response.status_code})."
    except Exception as e:
        print(f"[Groq Exception] {e}")
        return "Error procesando mi pensamiento artificial. 🧠💤"
        
# --- PROCESADOR DE COMANDOS COMÚN ---
def procesar_comandos(mensaje_completo, autor, plataforma):
    msg_lower = mensaje_completo.lower()
    
    if msg_lower == '!hola':
        return f"¡Hola @{autor}! Bienvenido al directo. Escribe !comandos para ver qué más puedo hacer. 🚀"
    elif msg_lower == '!discord':
        return f"@{autor} ¡Únete a nuestra comunidad y prueba la Actividad de Twitchion en Discord! 🎮✨"
    elif msg_lower == '!redes':
        return f"@{autor} Sigue nuestros canales y apoya el código libre! 🔥"
    elif msg_lower in ['!proyecto', '!twitchion']:
        return f"@{autor} Twitchion es la plataforma web de streaming descentralizada y optimizada para Discord. 💻🚀"
    elif msg_lower == '!comandos':
        return f"@{autor} Comandos: !hola, !discord, !redes, !proyecto, !github | O mencióname con @twichionBOT [tu pregunta] para hablar con mi IA. 🤖"
    elif msg_lower == '!github':
        return f"@{autor} Revisa los repositorios open-source de la comunidad en GitHub. ¡Todo hecho a puro código! 🛠️"
    elif '@twichionbot' in msg_lower:
        prompt_limpio = mensaje_completo.replace('@twichionbot', '').replace('@twichionBOT', '').strip()
        if prompt_limpio:
            print(f"[{plataforma}] Consultando Groq para {autor}...")
            return f"@{autor} {consultar_ia_groq(prompt_limpio, autor, plataforma)}"
        return f"@{autor} ¡Dime algo después de mencionarme para poder responderte con mi IA! 🤖"
    
    return None

# --- BUCLE DE TWITCH (HILO 1) ---
def iniciar_bot_twitch():
    sock = socket.socket()
    try:
        sock.connect((SERVER_TWITCH, PORT_TWITCH))
        sock.send(f"PASS {TOKEN_TWITCH}\r\n".encode('utf-8'))
        sock.send(f"NICK {NICKNAME_TWITCH}\r\n".encode('utf-8'))
        
        # Unirse a múltiples canales separados por comas
        canales_join = ",".join(CHANNELS_TWITCH)
        sock.send(f"JOIN {canales_join}\r\n".encode('utf-8'))
        print(f"[Twitch] Conectado exitosamente a {CHANNELS_TWITCH}")
        
        while True:
            response = sock.recv(2048).decode('utf-8', errors='ignore')
            if response.startswith('PING'):
                sock.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
                continue
                
            if "PRIVMSG" in response:
                partes = response.split('!')
                autor = partes[0][1:]
                
                # Parseo seguro del canal de origen y el mensaje
                partes_msg = response.split('PRIVMSG ')
                canal_origen = partes_msg[1].split(' :', 1)[0].strip()
                mensaje_completo = partes_msg[1].split(' :', 1)[1].strip()
                
                respuesta = procesar_comandos(mensaje_completo, autor, "Twitch")
                if respuesta:
                    # Responder específicamente al canal donde se escribió el mensaje
                    sock.send(f"PRIVMSG {canal_origen} :{respuesta}\r\n".encode('utf-8'))
    except Exception as e:
        print(f"[Twitch Error] {e}")

# --- BUCLE DE KICK (HILO 2) ---
async def bucle_kick():
    # Inicialización usando las variables de Kick
    kick_client = KickAPI(client_id=KICK_CLIENT_ID, token=KICK_TOKEN)
    
    @kick_client.on_message
    async def on_message(chat_message):
        if chat_message.sender.username.lower() == NICKNAME_TWITCH.lower():
            return
            
        autor = chat_message.sender.username
        texto_mensaje = chat_message.content
        
        respuesta = procesar_comandos(texto_mensaje, autor, "Kick")
        if respuesta:
            await kick_client.send_message(chat_message.chatroom_id, respuesta)

    for streamer in KICK_STREAMERS:
        print(f"[Kick] Conectando de forma segura al canal de {streamer}...")
    await kick_client.start(KICK_STREAMERS)

def iniciar_bot_kick():
    asyncio.run(bucle_kick())

# --- ORQUESTADOR PRINCIPAL ---
if __name__ == '__main__':
    # 1. Hilo del Servidor Web (Render)
    hilo_web = threading.Thread(target=iniciar_servidor_web, daemon=True)
    hilo_web.start()

    # 2. Hilo de Kick
    hilo_kick = threading.Thread(target=iniciar_bot_kick, daemon=True)
    hilo_kick.start()

    # 3. Hilo Principal: Twitch
    iniciar_bot_twitch()
