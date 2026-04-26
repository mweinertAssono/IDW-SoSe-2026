# Erweiterungsanleitung — Die App erweitern

Diese Anleitung zeigt, wie man die smolagents-App natürlich erweitert: **Tools hinzufügen**, **Multi-Agent-Workflows bauen** und **was noch wichtig ist**.

---

## 1. Tools hinzufügen

### Der einfache Weg: `@tool`-Decorator

Öffne `tools.py` und füge direkt vor `get_tools()` eine neue Funktion ein:

```python
from smolagents import tool

@tool
def calculate_tax(amount: float, rate: float) -> str:
    """Berechnet die Steuer auf einen Betrag.

    Args:
        amount: Der Basisbetrag (z. B. 100 Euro)
        rate: Der Steuersatz als Dezimalzahl (z. B. 0.19 für 19%)
    """
    tax = amount * rate
    total = amount + tax
    return f"Betrag: {amount:.2f}€ | Steuer ({rate*100:.0f}%): {tax:.2f}€ | Gesamt: {total:.2f}€"


# Später in get_tools():
def get_tools(settings: Settings) -> list[Any]:
    tools: list[Any] = [
        DuckDuckGoSearchTool(...),
        calculate_tax,  # ← hier einfach hinzufügen
    ]
    ...
```

**Warum das funktioniert:** Der `@tool`-Decorator extrahiert automatisch:

- Den Funktionsnamen → Name für den Agenten
- Den Docstring → Beschreibung (erste Zeile) + Argumente
- Die Typhinweise (`float`, `str`) → Parameter-Typen

### Der professionelle Weg: Tool-Klasse

Für komplexere Tools mit Konfiguration oder Zustand:

```python
from smolagents import Tool

class DatabaseTool(Tool):
    name = "database_search"
    description = "Sucht in unserer Datenbank nach Produkten und Preisen"
    inputs = {
        "query": {
            "type": "string",
            "description": "Suchbegriff (z. B. 'Laptop unter 1000 Euro')"
        },
        "category": {
            "type": "string",
            "description": "Kategorie filtern (optional)",
            "nullable": True,
        }
    }
    output_type = "string"

    def __init__(self, db_connection):
        super().__init__()
        self.db = db_connection  # ← Zustand speichern

    def forward(self, query: str, category: str = None) -> str:
        # Echte DB-Abfrage hier
        results = self.db.search(query, category)
        return f"Gefunden: {len(results)} Produkte\n" + "\n".join(results)


# In get_tools():
def get_tools(settings: Settings) -> list[Any]:
    db = connect_to_database()  # deine DB
    tools: list[Any] = [
        DuckDuckGoSearchTool(...),
        DatabaseTool(db),
    ]
    ...
```

---

## 2. Tools aktivieren

Aktuell sind die Tools in `agent_builder.py` deaktiviert:

```python
def build_agent(model: object, settings: Settings) -> ToolCallingAgent:
    return ToolCallingAgent(tools=[], model=model, stream_outputs=True)
    #     ↑ leere Liste!
```

Um Tools zu aktivieren, kommentiere diese Zeile ein:

```python
def build_agent(model: object, settings: Settings) -> ToolCallingAgent:
    return ToolCallingAgent(tools=get_tools(settings), model=model, stream_outputs=True)
    #                             ↑ jetzt mit Tools!
```

Der Agent kann jetzt deine Tools selbstständig aufrufen.

---

## 3. Multi-Agent-Workflows

Statt einen allmächtigen Agenten zu haben, kannst du spezialisierte Agenten bauen, die zusammenarbeiten.

### Beispiel: Such-Agent + Auswertungs-Agent

```python
from smolagents import ToolCallingAgent, DuckDuckGoSearchTool

# agent_builder.py
def build_agent(model: object, settings: Settings) -> ToolCallingAgent:

    # Spezialisierter Agent 1: Websuche
    search_agent = ToolCallingAgent(
        tools=[DuckDuckGoSearchTool()],
        model=model,
        name="search_specialist",
        description="Führt Websuchen durch und findet aktuelle Informationen",
        max_steps=3,
    )

    # Manager-Agent: koordiniert den Such-Agent
    manager = ToolCallingAgent(
        tools=[],
        model=model,
        managed_agents=[search_agent],  # ← Der Manager kann den Such-Agent aufrufen
        max_steps=5,
        instructions=(
            "When calling a sub-agent, use the 'task' parameter. "
            "Example: search_specialist(task='your query here')"
        ),
    )

    return manager
```

Jetzt kann der Manager dem Such-Agent Aufgaben delegieren:

**Nutzer:** _"Finde die neuesten Nachrichten zu KI-Agenten und fasse sie zusammen"_

1. Manager erkennt: "Das braucht eine Websuche"
2. Manager ruft auf: `search_specialist(task="KI-Agenten Nachrichten")`
3. Such-Agent führt Suche durch
4. Manager fasst Ergebnisse zusammen

---

## 4. Was sonst noch wichtig ist

### A. Fehlerbehandlung

Tools können fehlschlagen. Der Agent sollte das handhaben:

```python
@tool
def external_api_call(endpoint: str) -> str:
    """Ruft eine externe API auf."""
    import requests
    try:
        response = requests.get(f"https://api.example.com/{endpoint}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        return "FEHLER: API antwortet nicht (Timeout nach 5s)"
    except requests.HTTPError as e:
        return f"FEHLER: API gab Fehler zurück: {e.status_code}"
    except Exception as e:
        return f"FEHLER: Unerwarteter Fehler: {str(e)}"
```

### B. Streaming-Ausgabe (schon implementiert)

`stream_outputs=True` zeigt die Antwort Stück für Stück. Das verbessert die UX:

```python
ToolCallingAgent(
    tools=...,
    model=model,
    stream_outputs=True,  # ← "Echtzeitantwort" statt warten
)
```

### C. Max Steps begrenzen

Ein Agent kann in einer Endlosschleife stecken bleiben. Das verhindert man:

```python
ToolCallingAgent(
    tools=[...],
    model=model,
    max_steps=10,  # ← Nach 10 Schritten beenden, egal ob fertig oder nicht
)
```

Typische Werte:

- Einfache Aufgaben: `max_steps=3`
- Komplexe Recherchen: `max_steps=10`
- Multi-Agent: `max_steps=20` (Manager) + `max_steps=5` (Sub-Agents)

### D. System-Prompts anpassen

Du kannst den Agent instruieren:

```python
ToolCallingAgent(
    tools=[...],
    model=model,
    instructions=(
        "You are a helpful assistant. Always respond in German. "
        "Format your answers with markdown. "
        "If unsure, ask the user for clarification."
    ),
)
```

### E. State Management (für den nächsten Schritt)

Die aktuelle App vergisst jeden Chat nach Neustart. Für ein "echtes" System brauchst du:

- **Persistenz:** Chat-Verlauf in einer Datenbank speichern
- **User-Sessions:** Verschiedene Nutzer isolieren
- **Context-Fenster:** Alte Messages entfernen, um Kosten zu sparen

→ Das ist ein größeres Thema — für Anfänger nicht nötig.

---

## 5. Workflow: Neues Tool von Anfang bis Ende

1. **Tool in `tools.py` schreiben**

   ```python
   @tool
   def mein_werkzeug(...) -> str:
       """Beschreibung."""
       ...
   ```

2. **Tools aktivieren in `agent_builder.py`**

   ```python
   return ToolCallingAgent(tools=get_tools(settings), ...)
   ```

3. **Testen**

   ```bash
   python main.py
   # Im Gradio-Interface: "Nutze mein_werkzeug um..."
   ```

4. **Bei Problemen debuggen**
   - Terminal-Ausgabe anschauen — der Agent zeigt seine Gedanken
   - `max_steps` erhöhen wenn der Agent zu früh abbricht
   - Tool-Beschreibung klarer machen (der Agent liest nur den Docstring!)

---

## 6. Inspirierende Erweiterungs-Ideen

| Idee                            | Schwierigkeit | Nutzen                           |
| ------------------------------- | ------------- | -------------------------------- |
| CSV-Daten analysieren           | ⭐            | Agenten können Daten verarbeiten |
| Lokale Dateien lesen            | ⭐            | RAG without ML                   |
| E-Mail senden                   | ⭐⭐          | Agent kann kommunizieren         |
| Kalkulator mit mehr Funktionen  | ⭐⭐          | Mathematik-Agent                 |
| Weather API integrieren         | ⭐⭐          | Echte externe Daten              |
| Multi-Agent mit Spezialisierung | ⭐⭐⭐        | Skaliert zu komplexen Aufgaben   |
| Agenten-Memory (Embeddings)     | ⭐⭐⭐        | Agent lernt vom Verlauf          |

---

## 7. Ressourcen

- [smolagents Docs — Tools](https://huggingface.co/docs/smolagents/tutorials/tools)
- [smolagents Docs — Multi-Agent](https://huggingface.co/docs/smolagents/tutorials/multi_agent)
- [smolagents Docs — Best Practices](https://huggingface.co/docs/smolagents/tutorials/building_good_agents)
- [MCP Catalog](https://hub.docker.com/catalogs/mcp) — 300+ fertige Tools via Docker

Viel Erfolg! 🚀
