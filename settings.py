# -----------------------------------------------------------------------------
# settings.py – Konfiguration laden und validieren
#
# Diese Datei ist der erste Baustein unserer Anwendung.
# Sie liest alle nötigen Einstellungen aus Umgebungsvariablen (z. B. einer .env-Datei)
# und stellt sie als typisiertes Python-Objekt bereit.
# Das hat einen großen Vorteil: Der Rest des Programms muss sich nicht darum kümmern,
# woher ein Wert kommt – er bekommt ihn einfach übergeben.
# Dieses Muster nennt sich "Dependency Injection" und ist ein Grundprinzip
# sauberer Software-Architektur.
# -----------------------------------------------------------------------------

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


# Settings ist ein sogenanntes "Dataclass"-Objekt.
# Dataclasses sind eine elegante Python-Funktionalität (ab Python 3.7),
# um strukturierte Daten mit wenig Boilerplate zu definieren.
# Jedes Feld entspricht einer Konfigurationsvariable unserer App.
# Typen wie `str` und `bool` helfen uns und unseren Werkzeugen (IDE, Linter),
# Fehler früh zu erkennen – noch bevor das Programm überhaupt startet.
@dataclass
class Settings:
    llm_backend: str = "openrouter"                              # "openrouter" oder "ollama"
    openrouter_api_key: str = ""
    openrouter_model_id: str = "nvidia/nemotron-3-super-120b-a12b:free"
    ollama_model_id: str = "gemma4:26b"
    ollama_api_base: str = "http://localhost:11434/v1"
    ddg_max_results: int = 5
    gradio_share: bool = False
    use_docker_mcp: bool = False


# load_settings() – der einzige Weg, um an die Konfiguration zu kommen.
#
# Warum eine eigene Funktion dafür? Weil wir so die gesamte Lese-Logik
# an einem einzigen Ort bündeln. Wenn sich z. B. ein Variablenname ändert,
# müssen wir nur hier nachsehen.
#
# Ablauf:
#   1. python-dotenv lädt die .env-Datei in die Umgebungsvariablen (os.environ).
#   2. os.environ.get() liest jeden Wert – mit einem sinnvollen Standard-Fallback.
#   3. Der API-Key wird explizit geprüft, weil ohne ihn gar nichts funktioniert.
#   4. Das fertige Settings-Objekt wird zurückgegeben.
#
# Tipp fürs Labor: Ihr könnt hier einfach neue Felder ergänzen,
# wenn eure eigene Anwendung weitere Einstellungen braucht.
def load_settings() -> Settings:
    load_dotenv()

    llm_backend = os.getenv("LLM_BACKEND", "openrouter")

    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if llm_backend == "openrouter" and not api_key:
        raise RuntimeError("Missing OPENROUTER_API_KEY (wird bei LLM_BACKEND=openrouter benötigt)")

    return Settings(
        llm_backend=llm_backend,
        openrouter_api_key=api_key,
        openrouter_model_id=os.getenv("OPENROUTER_MODEL_ID", "nvidia/nemotron-3-super-120b-a12b:free"),
        ollama_model_id=os.getenv("OLLAMA_MODEL_ID", "gemma4:26b"),
        ollama_api_base=os.getenv("OLLAMA_API_BASE", "http://localhost:11434/v1"),
        ddg_max_results=int(os.getenv("DDG_MAX_RESULTS", "5")),
        gradio_share=os.getenv("GRADIO_SHARE", "false").lower() == "true",
        use_docker_mcp=os.getenv("USE_DOCKER_MCP", "false").lower() == "true",
    )
