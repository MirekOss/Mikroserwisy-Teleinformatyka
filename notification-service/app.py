# notification-service/app.py

# Użycie eventlet jako asynchronicznego silnika współbieżności – niezbędne do działania Socket.IO z Flaskiem
import eventlet
eventlet.monkey_patch()  # MUSI być wykonany jako pierwszy, by zmodyfikować standardowe biblioteki I/O

from flask import Flask, request, jsonify
from flask_socketio import SocketIO  # Dodaje obsługę WebSocketów do aplikacji Flask
from flask_cors import CORS          # Zezwala na żądania CORS z innych źródeł (np. frontend)
import time

app = Flask(__name__)
CORS(app)  # Pozwala na połączenia z dowolnego źródła (np. localhost:5500)
socketio = SocketIO(app, cors_allowed_origins="*")  # Inicjalizacja Socket.IO z pełnym CORS

# Prosty endpoint testowy – pomocny do sprawdzenia, czy serwis działa
@app.route("/")
def index():
    return "Notification service is running."

# Główny endpoint REST do odbierania powiadomień od innych mikroserwisów (np. peak-service)
@app.route("/api/notify", methods=["POST"])
def notify():
    data = request.get_json()
    msg = data.get("message")  # Pobranie treści powiadomienia z JSON-a

    print(f"📢 Otrzymano powiadomienie: {msg}")

    # Emituj zdarzenie WebSocket „new_event” do wszystkich podłączonych klientów (frontendów)
    # Dane (msg) trafiają do klienta w formie {"text": "..."}
    socketio.emit("new_event", {"text": msg})
    
    return jsonify({"message": "Powiadomienie wysłane"}), 200

# Obsługa zdarzenia połączenia WebSocket – rejestruje klienta
@socketio.on("connect")
def handle_connect():
    print("Klient połączony z WebSocket")

# Uruchomienie aplikacji z obsługą Socket.IO na porcie 5003
# socketio.run() działa podobnie do app.run(), ale wspiera komunikację WebSocket
if __name__ == "__main__":
    socketio.run(app, port=5003)
