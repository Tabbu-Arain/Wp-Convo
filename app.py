from flask import Flask, render_template
import subprocess
import os

app = Flask(__name__)

# Start Node.js process
node_process = subprocess.Popen(
    ["node", "whatsapp_node/index.js"],
    cwd=os.getcwd(),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

@app.route("/")
def home():
    return render_template("index.html")  # Now renders HTML instead of JSON

@app.route("/status")  # New endpoint for status checks
def status():
    return {
        "status": "running",
        "node_pid": node_process.pid
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
