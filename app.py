from flask import Flask, request, jsonify, render_template
import os
import asyncio
from baileys import WhatsApp  # Assuming you have a Python Baileys wrapper

app = Flask(__name__)

# Configuration
SESSION_DIR = "auth_session"
os.makedirs(SESSION_DIR, exist_ok=True)

# Initialize WhatsApp client
wa = WhatsApp(session_path=SESSION_DIR)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
async def send_message():
    try:
        data = request.json
        
        # Required parameters
        target = data["number"] + "@s.whatsapp.net"
        message = data["message"]
        delay = int(data.get("delay", 1))  # Default 1 second delay
        
        # Ensure connection
        if not wa.is_connected():
            return jsonify({"qr": wa.get_qr()}), 200
        
        # Send message
        await asyncio.sleep(delay)  # Respect delay
        await wa.send_message(target, message)
        
        return jsonify({
            "success": True,
            "message": "Message sent successfully"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
