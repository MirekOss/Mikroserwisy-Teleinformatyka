# notification-service/app.py
# Użycie eventlet dla lepszej obsługi SocketIO na Flasku
import eventlet
eventlet.monkey_patch()  # MUSI być jako pierwszy

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return "Notification service is running."

@app.route("/api/notify", methods=["POST"])
def notify():
    data = request.get_json()
    msg = data.get("message")

    print(f"📢 Otrzymano powiadomienie: {msg}")
    socketio.emit("new_entry", {"text": msg})
    
    return jsonify({"message": "Powiadomienie wysłane"}), 200

@socketio.on("connect")
def handle_connect():
    print("Klient połączony z WebSocket")

if __name__ == "__main__":
    socketio.run(app, port=5003)
