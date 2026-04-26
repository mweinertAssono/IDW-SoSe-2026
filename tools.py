# -----------------------------------------------------------------------------
# tools.py – Werkzeuge für den Agenten definieren
#
# Ein LLM-Agent ist nur so mächtig wie die Werkzeuge, die er nutzen kann.
# Ohne Werkzeuge kann er nur auf sein Training zurückgreifen – kein Internet,
# keine aktuellen Daten, keine externen Dienste.
# Mit Werkzeugen kann er suchen, rechnen, APIs aufrufen, Dateien lesen ...
# praktisch alles, was ihr als Python-Funktion ausdrücken könnt.
#
# smolagents macht es einfach, eigene Werkzeuge zu schreiben:
# Einfach eine Klasse von BaseTool ableiten oder den @tool-Decorator nutzen.
# Diese Datei ist euer zentraler Erweiterungspunkt für den zweiten Tag!
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# REFERENZ: Eingebaute smolagents-Werkzeuge (Stand: v1.23.0)
# Alle Tools unten können einfach importiert und in die tools-Liste eingefügt werden.
#
# ── Suche & Information ──────────────────────────────────────────────────────
#
#   DuckDuckGoSearchTool     – Websuche, kein API-Key nötig ✅ (aktiv unten)
#                              DuckDuckGoSearchTool(max_results=5, rate_limit=2.0)
#
#   WikipediaSearchTool      – Wikipedia-Artikel abrufen, kein API-Key nötig ✅
#                              from smolagents import WikipediaSearchTool
#                              WikipediaSearchTool(language="de", content_type="summary")
#
# ── Web-Interaktion ──────────────────────────────────────────────────────────
#
#   VisitWebpageTool         – Webseite öffnen und Inhalt als Text zurückgeben ✅
#                              Perfekt, um Links aus Suchergebnissen zu lesen.
#                              from smolagents import VisitWebpageTool
#                              VisitWebpageTool(max_output_length=40000)
#
# ── Code-Ausführung ──────────────────────────────────────────────────────────
#
#   PythonInterpreterTool    – Python-Code vom Agenten dynamisch ausführen lassen ✅
#                              Achtung: Kein Sicherheits-Sandkasten – nur lokal nutzen!
#                              from smolagents import PythonInterpreterTool
#                              PythonInterpreterTool(authorized_imports=["math", "json"])
#
# ── Nutzer-Interaktion ───────────────────────────────────────────────────────
#
#   UserInputTool            – Agent kann den Nutzer um Rückfragen bitten ✅
#                              Aktiviert "Human-in-the-Loop"-Workflows.
#                              from smolagents import UserInputTool
#                              UserInputTool()
#
# ── Sprache & Audio ──────────────────────────────────────────────────────────
#
#   SpeechToTextTool         – Audio transkribieren via Whisper
#                              Benötigt: transformers + ein Whisper-Modell lokal
#                              from smolagents import SpeechToTextTool
#                              SpeechToTextTool()
#
# -----------------------------------------------------------------------------
# EIGENE WERKZEUGE ERSTELLEN
#
#   Variante A: @tool-Decorator (empfohlen für einfache Funktionen)
#
#       from smolagents import tool
#
#       @tool
#       def mein_werkzeug(eingabe: str) -> str:
#           """Kurze Beschreibung – der Agent liest genau das!
#           Args:
#               eingabe: Was dieses Argument bedeutet.
#           """
#           return f"Ergebnis: {eingabe}"
#
#   Variante B: Tool-Klasse (für Werkzeuge mit Zustand oder mehreren Methoden)
#
#       from smolagents import Tool
#
#       class MeinWerkzeug(Tool):
#           name = "mein_werkzeug"
#           description = "Kurze Beschreibung für den Agenten."
#           inputs = {"eingabe": {"type": "string", "description": "..."}}
#           output_type = "string"
#
#           def forward(self, eingabe: str) -> str:
#               return f"Ergebnis: {eingabe}"
#
# -----------------------------------------------------------------------------

from __future__ import annotations

import os
from typing import Any

from mcp import StdioServerParameters
from smolagents import DuckDuckGoSearchTool, ToolCollection

from settings import Settings

# Maximale Zeichenanzahl für Werkzeug-Ausgaben, die ans Modell gehen.
# DuckDuckGo-Suchergebnisse können sehr lang werden und das Token-Budget
# überfluten. 3 000 Zeichen reichen für eine gute Zusammenfassung.
MAX_TOOL_OUTPUT_CHARS = 3_000


class TruncatedDuckDuckGoSearchTool(DuckDuckGoSearchTool):
    """Wie DuckDuckGoSearchTool, kürzt aber die Ausgabe auf ein sicheres Maximum,
    damit das Modell nicht mit riesigen Textwänden überflutet wird."""

    def forward(self, query: str) -> str:
        result = super().forward(query)
        if len(result) > MAX_TOOL_OUTPUT_CHARS:
            return result[:MAX_TOOL_OUTPUT_CHARS] + "\n\n[... Ergebnis gekürzt ...]"
        return result


# get_tools() – stellt die Liste der verfügbaren Werkzeuge zusammen.
#
# Aktuell sind zwei Werkzeugquellen aktiv:
#   1. DuckDuckGoSearchTool – klassisches smolagents-Werkzeug, direkt in Python.
#   2. MCP über Docker      – externer Server, der als Container läuft.
#
# Mehr Ergebnisse beim DuckDuckGo = mehr Kontext für das Modell, aber auch
# höhere Token-Kosten. 5 ist ein guter Startpunkt.
#
# Ideen für eigene Werkzeuge (perfekt fürs Labor):
#   - Ein Werkzeug, das eine CSV-Datei einliest und auswertet
#   - Ein Werkzeug, das Bilder generiert (z. B. via Stable Diffusion API)
#   - Ein Werkzeug, das eine Datenbank abfragt
#   - Ein Werkzeug, das E-Mails oder Kalendereinträge liest
# Eurer Fantasie sind keine Grenzen gesetzt!
def get_tools(settings: Settings) -> list[Any]:
    tools: list[Any] = [
        TruncatedDuckDuckGoSearchTool(
            max_results=settings.ddg_max_results,
            rate_limit=2.0,
        )
    ]

    # -------------------------------------------------------------------------
    # MCP-Werkzeuge via Docker Desktop
    #
    # Was ist MCP? Model Context Protocol ist ein offener Standard, mit dem
    # KI-Agenten externe Dienste als Werkzeuge nutzen können – ähnlich wie
    # ein USB-Anschluss für Fähigkeiten. Jeder MCP-Server stellt eine Sammlung
    # von Werkzeugen bereit, die der Agent eigenständig aufrufen kann.
    #
    # Warum Docker? Docker isoliert den Server-Code in einem Container.
    # Kein Node.js installieren, keine Python-Konflikte, kein Aufräumen danach.
    # Docker Desktop muss laufen – das war's.
    #
    # Wie funktioniert das technisch?
    #   smolagents startet den Docker-Container als Kindprozess (stdio-Transport).
    #   Der Agent kommuniziert mit ihm über Standard-Ein-/Ausgabe (JSON-RPC).
    #   Beim Verlassen des `with`-Blocks wird der Container automatisch gestoppt.
    #
    # Welche MCP-Server gibt es?
    #   Über 300 fertige, verifiziierte Images im Docker MCP Catalog:
    #   https://hub.docker.com/catalogs/mcp
    #   Beispiele: GitHub, Notion, Playwright, Elasticsearch, MongoDB, Stripe ...
    #
    # Das Beispiel hier: mcp/fetch
    #   Gibt dem Agenten die Fähigkeit, beliebige URLs abzurufen und deren
    #   Inhalt als Text zurückzugeben. Kein API-Key nötig. ✅
    #   Docker Hub: https://hub.docker.com/r/mcp/fetch
    # -------------------------------------------------------------------------
    if settings.use_docker_mcp:
        mcp_server = StdioServerParameters(
            command="docker",
            args=[
                "run",
                "-i",       # Interaktiver Modus: Container liest von stdin
                "--rm",     # Container wird nach dem Stoppen automatisch gelöscht
                "mcp/fetch",
            ],
            env={**os.environ},  # Umgebungsvariablen an den Container weitergeben
        )

        try:
            with ToolCollection.from_mcp(mcp_server, trust_remote_code=True) as mcp_tools:
                # mcp_tools.tools ist eine Liste aller Werkzeuge, die der Server anbietet.
                # Wir fügen sie direkt zur tools-Liste hinzu – der Agent sieht sie wie
                # jedes andere smolagents-Werkzeug, ohne den Unterschied zu kennen.
                tools.extend(mcp_tools.tools)
        except Exception:
            # Docker läuft nicht oder das Image ist nicht verfügbar.
            # Kein Problem – wir starten trotzdem, nur ohne MCP-Tools.
            print("⚠️  MCP-Tools nicht verfügbar (Docker nicht erreichbar). Starte ohne MCP.")

    return tools
