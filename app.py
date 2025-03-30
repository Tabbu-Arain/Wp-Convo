from flask import Flask, render_template, request, jsonify
import os
import random
import asyncio
from threading import Thread
from maher_zubair_baileys import Gifted_Tech, useMultiFileAuthState, makeCacheableSignalKeyStore
import pino

app = Flask(__name__)

sessions = {}

# 🔥 Generate WhatsApp Pairing Code
async def generate_pair_code(number):
    try:
        session_id = f"session_{random.randint(1000, 9999)}"
        sessions[number] = session_id
        os.makedirs(f'./temp/{session_id}', exist_ok=True)

        state, saveCreds = await useMultiFileAuthState(f'./temp/{session_id}')

        bot = Gifted_Tech({
            "auth": {
                "creds": state.creds,
                "keys": makeCacheableSignalKeyStore(state.keys, pino.Logger(level="fatal"))
            },
            "printQRInTerminal": False,
            "logger": pino.Logger(level="fatal"),
            "browser": ["Chrome (Linux)", "", ""]
        })

        await asyncio.sleep(2)
        code = await bot.requestPairingCode(number)
        return code

    except Exception as e:
        return str(e)

# 🔥 Serve the Frontend (Default Page)
@app.route('/')
def home():
    return render_template('index.html', pairing_code=None)  # Default page without code

# 🔥 API to Get Pairing Code and Pass it to HTML
@app.route('/code', methods=['GET'])
def get_code():
    number = request.args.get("number")
    if not number:
        return render_template('index.html', pairing_code="Enter a valid number")

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        code = loop.run_until_complete(generate_pair_code(number))
        return render_template('index.html', pairing_code=code)
    except Exception as e:
        return render_template('index.html', pairing_code=str(e))

# 🔥 Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
