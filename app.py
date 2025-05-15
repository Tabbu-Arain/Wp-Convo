import os
import subprocess
from flask import Flask, jsonify

app = Flask(__name__)

# Start Node.js when Flask initializes
node_process = subprocess.Popen(
    ["node", "whatsapp_node/index.js"],
    cwd=os.getcwd(),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

@app.route("/")
def status():
    return jsonify({
        "status": "running",
        "node_pid": node_process.pid
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
