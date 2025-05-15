from flask import Flask, request, jsonify, render_template
import subprocess
import os
import threading
import time

app = Flask(__name__)

# Path to Node.js script
NODE_SCRIPT = os.path.join("whatsapp_node", "index.js")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_whatsapp():
    try:
        # Run Node.js script in background
        threading.Thread(
            target=subprocess.run,
            args=(["node", NODE_SCRIPT],),
            kwargs={"capture_output": True, "text": True}
        ).start()
        
        return jsonify({"status": "Node.js script started"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    target = data.get("number")
    message = data.get("message")
    
    if not target or not message:
        return jsonify({"error": "Missing number/message"}), 400
    
    try:
        # Send message via Node.js (example - adapt to your Node script)
        result = subprocess.run(
            ["node", "whatsapp_node/send.js", target, message],
            capture_output=True,
            text=True
        )
        return jsonify({"output": result.stdout})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
