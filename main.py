# -----------------------------------------------------------------------------
# main.py – der Dirigent unserer Anwendung
#
# Diese Datei ist bewusst schlank gehalten. Ihre einzige Aufgabe ist es,
# die vier Hauptschritte unserer App in der richtigen Reihenfolge aufzurufen.
# Dieses Prinzip – "thin orchestrator, fat modules" – macht Code übersichtlich
# und leicht testbar: Jedes Modul kann unabhängig getestet werden,
# ohne die ganze App starten zu müssen.
#
# Startet die App mit:
#   uv run smolagents-app
# oder direkt:
#   python main.py
# -----------------------------------------------------------------------------

import atexit

from agent_builder import build_agent
from gradio_ui import launch_gradio
from openrouter import create_model
from settings import load_settings
from tools import close_mcp


# main() – vier Schritte, eine Anwendung.
#
# Schritt 1 | Konfiguration laden
#   Alle Einstellungen kommen aus der .env-Datei oder den Umgebungsvariablen.
#   Kein hartcodierter API-Key, nirgends – das ist wichtig für Sicherheit
#   und Wiederverwendbarkeit (z. B. in Docker oder CI/CD).
#
# Schritt 2 | Modell erstellen
#   Wir verbinden uns mit OpenRouter und wählen das gewünschte Sprachmodell.
#   Hier könntet ihr auch ein lokales Modell (z. B. via Ollama) einbinden.
#
# Schritt 3 | Agenten bauen
#   Modell + Werkzeuge = handlungsfähiger Agent.
#   Ab hier kann die KI eigenständig Entscheidungen treffen.
#
# Schritt 4 | Oberfläche starten
#   Gradio öffnet einen lokalen Web-Server. Der Agent ist jetzt
#   über den Browser erreichbar – bereit für eure Fragen.
def main() -> None:
    settings = load_settings()

    model = create_model(settings)

    agent = build_agent(model, settings)

    # MCP-Verbindungen sauber schließen, wenn die App beendet wird.
    atexit.register(close_mcp)

    launch_gradio(agent, settings)


if __name__ == "__main__":
    main()


