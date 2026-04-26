# -----------------------------------------------------------------------------
# openrouter.py – Verbindung zum Sprachmodell herstellen
#
# OpenRouter ist ein Dienst, der euch Zugang zu Dutzenden verschiedener
# Sprachmodelle über eine einheitliche API gibt – darunter GPT-Modelle, Claude,
# Llama, Mistral und viele mehr.
# Das Praktische: Die API ist kompatibel mit dem OpenAI-Standard.
# Das bedeutet, smolagents (und fast jede andere LLM-Bibliothek) kann sie
# direkt nutzen, ohne spezielle Anpassungen.
# Ihr müsst euch nur einmal bei openrouter.ai registrieren und
# einen API-Key beantragen – das ist kostenlos für bestimmte Modelle.
# -----------------------------------------------------------------------------

from __future__ import annotations

import json_repair
from smolagents import OpenAIServerModel
from smolagents.models import MessageRole, get_tool_call_from_text

from settings import Settings


class RobustOpenAIServerModel(OpenAIServerModel):
    """Wie OpenAIServerModel, aber parse_tool_calls nutzt json_repair statt
    des Standard-JSON-Parsers. Korrigiert automatisch leichte JSON-Fehler
    in Modellantworten – z. B. unescapte Anführungszeichen oder Smart Quotes
    in langen Texten (häufig bei final_answer mit Fließtexten)."""

    def parse_tool_calls(self, message):
        message.role = MessageRole.ASSISTANT
        if not message.tool_calls:
            assert message.content is not None, "Message contains no content and no tool calls"
            message.tool_calls = [
                get_tool_call_from_text(message.content, self.tool_name_key, self.tool_arguments_key)
            ]
        assert len(message.tool_calls) > 0, "No tool call was found in the model output"
        for tool_call in message.tool_calls:
            args = tool_call.function.arguments
            if isinstance(args, str):
                tool_call.function.arguments = json_repair.loads(args)
        return message


# create_openrouter_model() – erzeugt den Modell-Client für OpenRouter.
#
# Was passiert hier genau?
#   - Wir erstellen ein OpenAI-kompatibles Modell-Objekt.
#   - Wir übergeben die base_url von OpenRouter statt der OpenAI-URL.
#   - API-Key und Modell-ID kommen aus unserem Settings-Objekt.
#
# Das Modell-Objekt selbst führt noch keine KI-Anfrage durch!
# Es ist nur eine konfigurierte Verbindung – vergleichbar mit dem
# Einrichten einer Datenbankverbindung, bevor man die erste Abfrage stellt.
#
# Welches Modell wollt ihr verwenden? Schaut euch die Liste an:
# https://openrouter.ai/models
# Ändert einfach OPENROUTER_MODEL_ID in eurer .env-Datei, um das Modell zu wechseln.
def create_openrouter_model(settings: Settings) -> RobustOpenAIServerModel:
    return RobustOpenAIServerModel(
        model_id=settings.openrouter_model_id,
        api_base="https://openrouter.ai/api/v1",
        api_key=settings.openrouter_api_key,
    )


# create_ollama_model() – erzeugt den Modell-Client für lokales Ollama.
#
# Ollama bietet dieselbe OpenAI-kompatible API wie OpenRouter –
# der einzige Unterschied ist die URL und dass kein echter API-Key nötig ist.
# Das Modell muss vorher lokal geladen sein: ollama pull <modell-id>
# Modell-Liste: https://ollama.com/library
def create_ollama_model(settings: Settings) -> RobustOpenAIServerModel:
    return RobustOpenAIServerModel(
        model_id=settings.ollama_model_id,
        api_base=settings.ollama_api_base,
        api_key="ollama",  # Pflichtfeld im Client, Inhalt wird von Ollama ignoriert
        # Gemma 4 empfohlene Sampling-Parameter (https://ollama.com/library/gemma4)
        temperature=1.0,
        top_p=0.95,
        extra_body={
            "options": {
                "top_k": 64,           # Ollama-spezifisch, Gemma-4-Empfehlung
                "num_ctx": 16384,      # Kontextfenster: verhindert Loop bei langen Texten
                "repeat_penalty": 1.3, # Wiederholunsstrafe: etwas aggressiver als Standard
                "repeat_last_n": -1,   # -1 = gesamtes Kontextfenster prüfen (kein blindes Fenster)
            }
        },
    )


# create_model() – wählt automatisch das richtige Backend.
#
# Das ist der Einstiegspunkt, den main.py aufruft.
# Er liest settings.llm_backend und erstellt das passende Modell-Objekt.
# So muss main.py nichts über die Details der Backends wissen.
def create_model(settings: Settings) -> RobustOpenAIServerModel:
    if settings.llm_backend == "ollama":
        print(f"🖥️  Backend: Ollama  |  Modell: {settings.ollama_model_id}")
        return create_ollama_model(settings)
    else:
        print(f"☁️  Backend: OpenRouter  |  Modell: {settings.openrouter_model_id}")
        return create_openrouter_model(settings)
