# Aplikacja Górska – mikroserwisy, GraphQL, WebSocket

Projekt demonstracyjny do celów dydaktycznych prezentujący architekturę mikroserwisową z użyciem REST, GraphQL i WebSocket. System umożliwa:

- dodawanie użytkowników,
- dodawanie wejść na szczyty,
- pobieranie listy szczytów wg dwóch kryteriów: województwo oraz wysokość (GraphQL),
- powiadomienia w czasie rzeczywistym (WebSocket).

---

## Struktura projektu

```
Spotkanie-6/
├── frontend/                 ← HTML + JS + Bootstrap + WebSocket
│   ├── index.html
│   └── js/
│       └── app.js
├── user-service/            ← REST API do rejestracji użytkowników
│   └── app.py
├── peak-service/            ← REST + GraphQL API do szczytów i wejść
│   ├── app.py
│   ├── mock_peaks.py
│   └── schema.py
├── notification-service/    ← WebSocket serwer emitujący powiadomienia
│   └── app.py
├── requirements.txt         ← Wspólne zależności (dla jednego venv)
└── README.txt
```

---

## Technologie

| Obszar           | Użyte rozwiązania                                             |
|------------------|---------------------------------------------------------------|
| Frontend         | HTML, JS (Fetch API, Socket.IO), Bootstrap                    |
| Backend API      | Flask (REST), Flask-CORS, Flask-SocketIO, Graphene  (GraphQL) |
| Komunikacja      | REST, GraphQL, WebSocket                                      |
| Architektura     | Mikroserwisy (3 serwisy backendowe + frontend)                |
| Powiadomienia    | socket.io emitowane przez `notification-service`              |

---
### Autoryzacja JWT
Projekt wykorzystuje mechanizm tokenów JWT (JSON Web Token) do autoryzacji dostępu do chronionych zasobów (np. dodawanie wejścia na szczyt):
- Po rejestracji użytkownika generowany jest token JWT, zawierający jego tożsamość (identity).
- Token ten jest przesyłany w nagłówku Authorization: Bearer ... przy kolejnych żądaniach.
- Backend (Flask) za pomocą @jwt_required() sprawdza ważność tokena i identyfikuje użytkownika przez get_jwt_identity().
- Dzięki temu dane użytkownika nie są przesyłane w treści żądań, a aplikacja pozostaje bezstanowa i bezpieczna.

Zabezpieczone zasoby:
- POST /api/add_entry – wymaga ważnego tokena
- POST /graphql – endpoint do danych także objęty autoryzacją

---

### Dodatkowe wyjaśnienie: Graphene (GraphQL)
Graphene to biblioteka Pythona umożliwiająca tworzenie elastycznych API opartych na GraphQL.
W projekcie `peak-service` wykorzystano ją do udostępnienia endpointu `/graphql`, który umożliwia:
- pobieranie danych o szczytach z opcjonalnym filtrowaniem (np. `minHeight`, `wojewodztwo`),
- precyzyjne określenie, które pola mają zostać zwrócone (np. tylko `name` i `height`),
- ograniczenie liczby żądań i zmniejszenie obciążenia serwera w porównaniu do klasycznego REST.

Graphene automatycznie dopasowuje zapytania do zdefiniowanego schematu (`schema.py`) i uruchamia funkcje typu `resolve_<pole>`, odpowiedzialne za logikę danych.

---

## Uruchamianie

### 1. Klonuj repozytorium / przygotuj katalog

```bash
git clone https://github.com/twoje/repo.git
cd Spotkanie-6
```

### 2. Utwórz środowisko wirtualne

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 4. Uruchom serwisy (każdy w osobnym terminalu lub powershellu)
(1)
```bash
# Terminal 1 – user-service
cd user-service
python app.py

# Terminal 2 – peak-service
cd peak-service
python app.py

# Terminal 3 – notification-service
cd notification-service
python app.py
```
(2)
Lub uruchom w powershell:
```bash
start-windows.ps1
```

### 5. Uruchom frontend

Otwórz plik `frontend/index.html` w przeglądarce:  
http://127.0.0.1:5500/index.html (np. przez rozszerzenie Live Server w VS Code)

---

## Co pokazuje projekt

| Element                | Realizacja                                                                            |
|------------------------|---------------------------------------------------------------------------------------|
| REST API               | `/api/add_user`, `/api/add_entry` – prosty model komunikacji                          |
| Bezpieczny dostęp      | Token JWT zapewnia autoryzację przy zapytaniach REST                                  |
| GraphQL API            | Elastyczne zapytania do danych, np. `query { peaks(minHeight: 1200) { name pasmo } }` |
| WebSocket              | Natychmiastowe powiadomienia przy zdarzeniach                                         |
| Mikroserwisy           | Niezależne serwisy do użytkowników, szczytów, powiadomień                             |
| Oddzielenie logiki     | Serwis źródłowy formatuje komunikat – frontend tylko go wyświetla                     |

---

## Wymagania systemowe

- Python 3.8+
- Przeglądarka obsługująca `fetch()` i `WebSocket` (np. Chrome, Firefox)
- Rekomendowane: VS Code + rozszerzenie **Live Server**

---

## Kontakt

Projekt stworzony na potrzeby kursu **Technologie webowe i języki skryptowe**.  


