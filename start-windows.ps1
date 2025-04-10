# Skrypt PowerShell do uruchamiania mikroserwisów aplikacji górskiej (Windows)
# Upewnij się, że jesteś w katalogu głównym projektu (Spotkanie-6)

Write-Host "Aktywacja środowiska virtualenv..."
.\venv\Scripts\Activate.ps1

Start-Process powershell -ArgumentList "-NoExit", "-Command cd user-service; Write-Host '✨ uruchamiam user-service'; python app.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command cd peak-service; Write-Host '⛰ uruchamiam peak-service'; python app.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command cd notification-service; Write-Host '🗣️ uruchamiam notification-service'; python app.py"

Write-Host "🚀 Wszystkie serwisy uruchomione w osobnych oknach PowerShell."
Write-Host "Otwórz frontend (index.html przez Live Server lub inny hosting) i testuj aplikację."
