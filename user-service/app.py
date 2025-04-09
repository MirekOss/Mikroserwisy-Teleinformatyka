# user-service/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
# pozwala na połączenia z localhost:5500
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.config["JWT_SECRET_KEY"] = "tajny-klucz-demo"
jwt = JWTManager(app)

# Tymczasowa "baza" użytkowników
users = []  # tymczasowa lista użytkowników

@app.route("/api/login", methods=["POST"])
def loginUser():
    # Pobierz dane JSON przesłane w żądaniu HTTP POST
    data = request.get_json()
    username = data.get("username")  # Odczytaj nazwę użytkownika z danych

    # Walidacja: jeśli nie podano nazwy użytkownika, zwróć błąd 400
    if not username:
        return jsonify({"message": "Brakuje nazwy użytkownika."}), 400

    # Tworzenie tokena JWT z identyfikatorem użytkownika (identity=username)
    # Token będzie później używany do autoryzacji (np. z @jwt_required)
    access_token = create_access_token(identity=username)

    # Przykład komunikacji między mikroserwisami – wysyłamy powiadomienie
    # do notification-service, że użytkownik się zalogował (lub zarejestrował)
    try:
        requests.post("http://localhost:5003/api/notify", json={
            "message": f"{username.capitalize()} zarejestrował(a) się"
        })
    except Exception as e:
        # Obsługa błędu, np. gdy notification-service nie działa
        print("❌ Błąd wysyłania powiadomienia:", e)

    # Zwróć klientowi token dostępu oraz potwierdzenie nazwy użytkownika
    return jsonify(access_token=access_token, username=username), 200

if __name__ == "__main__":
    app.run(port=5001, debug=True)