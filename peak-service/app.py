from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from graphene import Schema
from schema import Query
import requests

app = Flask(__name__)

schema = Schema(query=Query)

# ✅ KONKRETNA domena + credentials
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}}, supports_credentials=True)

app.config["JWT_SECRET_KEY"] = "tajny-klucz-demo"
jwt = JWTManager(app)

# ✅ HANDLER dla zapytań OPTIONS (preflight)
@app.route("/api/add_entry", methods=["OPTIONS"])
def options_entry():
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:5500")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 204

# Endpoint REST do rejestrowania wejścia użytkownika na szczyt
@app.route("/api/add_entry", methods=["POST"])
@jwt_required()  # 🔐 Wymaga autoryzacji – tylko użytkownicy z ważnym tokenem JWT mogą dodać wpis
def add_entry():
    # Pobranie danych z żądania POST w formacie JSON
    data = request.get_json()

    # Odczyt tożsamości użytkownika z tokena JWT (została tam zapisana przy logowaniu)
    user = get_jwt_identity()

    # Odczyt nazwy szczytu z danych przesłanych przez użytkownika
    peak = data.get("peak")

    # Walidacja danych – brakujący użytkownik lub szczyt → błąd 400
    if not peak or not user:
        return jsonify({"message": "Brak danych"}), 400

    # Komunikacja z notification-service – wysłanie powiadomienia o zdobyciu szczytu
    try:
        requests.post("http://localhost:5003/api/notify", json={
            "message": f"{user.capitalize()} zdobył(a) szczyt {peak}"
        })
    except Exception as e:
        # Obsługa ewentualnego błędu przy próbie wysłania powiadomienia
        print("❌ Błąd notyfikacji:", e)

    # Zwrócenie potwierdzenia dodania wpisu
    return jsonify({"message": f"Dodano wejście: {user.capitalize()} - {peak}"}), 200

@app.route("/graphql", methods=["POST"])
def graphql_endpoint():
    """
    Endpoint GraphQL obsługujący zapytania POST z danymi JSON.
    Oczekuje pola 'query' zawierającego zapytanie GraphQL.
    """
    data = request.get_json()

    # Obsługa błędu gdy brak zapytania
    if not data or "query" not in data:
        return jsonify({"error": "Brak zapytania GraphQL w ciele żądania."}), 400

    # Wykonanie zapytania na podstawie zdefiniowanego schematu
    result = schema.execute(
        data["query"],
        variables=data.get("variables"),
        context_value=request  # możesz przekazać kontekst (np. auth info)
    )

    # Obsługa błędów wykonania zapytania
    response_data = {}
    if result.errors:
        response_data["errors"] = [str(e) for e in result.errors]
    if result.data:
        response_data["data"] = result.data

    return jsonify(response_data)


if __name__ == "__main__":
    app.run(port=5002, debug=True)
