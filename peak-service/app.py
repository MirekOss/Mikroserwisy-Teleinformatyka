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

# ✅ Główna logika wpisu
@app.route("/api/add_entry", methods=["POST"])
@jwt_required()
def add_entry():
    data = request.get_json()
    user = get_jwt_identity()
    peak = data.get("peak")

    if not peak or not user:
        return jsonify({"message": "Brak danych"}), 400

    try:
        requests.post("http://localhost:5003/api/notify", json={
            "message": f"{user.capitalize()} zdobył(a) szczyt {peak}"
        })
    except Exception as e:
        print("❌ Błąd notyfikacji:", e)

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
