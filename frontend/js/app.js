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

// Logowanie i pobieranie tokena JWT
const loginUser = async () => {
    const username = document.getElementById("username").value;
    const response = await fetch("http://localhost:5001/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username })
    });

    const result = await response.json();
    jwtToken = result.access_token;

    document.getElementById("userStatus").textContent = `Zalogowano jako: ${result.username}`;
};

const addEntry = async () => {
    const peak = document.getElementById("entryPeak").value;

    if (!jwtToken) {
        alert("Musisz się najpierw zalogować.");
    }

    const response = await fetch("http://localhost:5002/api/add_entry", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${jwtToken}`
        },
        body: JSON.stringify({ peak })
    });

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