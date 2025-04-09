// js/app.js
document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();             // zatrzymuje wysyłanie formularza
    const form = e.target;
    form.classList.add("was-validated"); // <- ZAWSZE dodaj klasę
    if (!form.checkValidity()) {   // uruchamia HTML5/Bootstrap walidację
        return;
    }

    await loginUser();             // jeśli wszystko ok → logowanie
});

let jwtToken = null;

// Logowanie i pobieranie tokena JWT z backendu
const loginUser = async () => {
    // Pobierz nazwę użytkownika wpisaną w formularzu
    const username = document.getElementById("username").value;

    // Wyślij zapytanie POST do endpointu logowania (/api/login) w user-service
    const response = await fetch("http://localhost:5001/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username })  // Przekazanie danych jako JSON
    });

    // Odbierz odpowiedź z tokenem JWT i nazwą użytkownika
    const result = await response.json();

    // Zapisz token JWT do zmiennej globalnej (może być używany w przyszłych żądaniach)
    jwtToken = result.access_token;

    // Zaktualizuj interfejs: pokaż informację o zalogowanym użytkowniku
    document.getElementById("userStatus").textContent = `Zalogowano jako: ${result.username}`;
};

// Wysyłanie informacji o zdobyciu szczytu – chronione zapytanie do backendu
const addEntry = async () => {
    // Pobierz nazwę szczytu wpisaną przez użytkownika z formularza
    const peak = document.getElementById("entryPeak").value;

    // Sprawdź, czy użytkownik jest zalogowany (czy posiada token JWT)
    if (!jwtToken) {
        alert("Musisz się najpierw zalogować.");  // prosta walidacja klienta
        return;  // przerwij działanie funkcji
    }

    // Wyślij żądanie POST do chronionego endpointu `/api/add_entry` w serwisie peak-service
    const response = await fetch("http://localhost:5002/api/add_entry", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",  // informacja, że dane są w formacie JSON
            "Authorization": `Bearer ${jwtToken}` // dołączenie tokena JWT w nagłówku autoryzacyjnym
        },
        body: JSON.stringify({ peak })  // dane przesyłane do API – nazwa zdobytego szczytu
    });

    // Odbierz odpowiedź z serwera i wyświetl ją użytkownikowi
    const result = await response.json();
    document.getElementById("entryStatus").textContent = `${result.message}`;
};

// Pobierz szczyty z minimalną wysokością
async function fetchPeaksByMinHeight(minHeight) {
    const query = `
      query {
        peaks(minHeight: ${minHeight}) {
          name
          height
          pasmo
          wojewodztwo
        }
      }
    `;
  
    const response = await fetch("http://localhost:5002/graphql", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
  
    const result = await response.json();
    renderPeaksByMinHeight(result.data.peaks);
}
  
  // Pobierz szczyty z danego województwa
  async function fetchPeaksByWojewodztwo(wojewodztwo) {
    const query = `
      query {
        peaks(wojewodztwo: "${wojewodztwo}") {
          name
          height
          pasmo
          wojewodztwo
        }
      }
    `;
  
    const response = await fetch("http://localhost:5002/graphql", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
  
    const result = await response.json();
    renderPeaksByWojewodztwo(result.data.peaks);
  }
  
  // Funkcje pomocnicze do renderowania wyników
  function renderPeaksByMinHeight(peaks) {
    const list = document.getElementById("peak-list-height");
    renderListToElement(peaks, list);
  }
  
  function renderPeaksByWojewodztwo(peaks) {
    const list = document.getElementById("peak-list-wojewodztwo");
    renderListToElement(peaks, list);
  }
  
  function renderListToElement(peaks, container) {
    container.innerHTML = "";
  
    if (peaks.length === 0) {
      container.innerHTML = "<li>Brak wyników spełniających kryteria.</li>";
      return;
    }
  
    peaks.forEach((peak) => {
      const item = document.createElement("li");
      item.textContent = `${peak.name} (${peak.height} m) – ${peak.pasmo}, woj. ${peak.wojewodztwo}`;
      container.appendChild(item);
    });
  }


// WebSocket - Socket.IO
const socket = io("http://localhost:5003");
const notifications = document.getElementById("notifications");

socket.on("connect", () => {
    console.log("Połączono z WebSocket");
});

socket.on("new_entry", (data) => {
    const div = document.createElement("div");
    div.textContent = data.text;
    notifications.prepend(div);
});