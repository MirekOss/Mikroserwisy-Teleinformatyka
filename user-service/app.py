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
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"message": "Brakuje nazwy użytkownika."}), 400

    access_token = create_access_token(identity=username)
    # Wyślij powiadomienie do notification-service
    try:
        requests.post("http://localhost:5003/api/notify", json={
            "message": f"{username.capitalize()} zarejestrował(a) się"
        })
    except Exception as e:
        print("❌ Błąd wysyłania powiadomienia:", e)
        
    return jsonify(access_token=access_token, username=username), 200

if __name__ == "__main__":
    app.run(port=5001, debug=True)