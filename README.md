# Einrichtungsanleitung — smolagents Intro App

Diese Anleitung führt dich Schritt für Schritt durch die Einrichtung des Projekts — sowohl für die Hauptanwendung als auch für das Jupyter Notebook `agents.ipynb`.

---

## Voraussetzungen

| Voraussetzung                   | Details                                                                                                                 |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Python**                      | Version 3.12 (genau — `pyproject.toml` erlaubt `>=3.12,<3.13`)                                                          |
| **Git**                         | Zum Klonen des Repos                                                                                                    |
| **OpenRouter-Account**          | Kostenlos unter [openrouter.ai](https://openrouter.ai) — für die App und das Notebook (OpenRouter-Backend)              |
| **Ollama**                      | Für das Notebook zwingend erforderlich (RAG-Embeddings laufen immer lokal) — [ollama.com](https://ollama.com)           |
| **Docker Desktop** _(optional)_ | Nur wenn du MCP-Server-Tools in `tools.py` nutzen willst — [docker.com](https://www.docker.com/products/docker-desktop) |

> **Python 3.12 installieren:**
>
> - **Windows:** `winget install Python.Python.3.12` oder Download von [python.org](https://www.python.org/downloads/release/python-3129/) — beim Installer „Add python.exe to PATH" aktivieren.
> - **Ubuntu 24.04+:** `sudo apt install python3.12 python3.12-venv`
> - **Ubuntu 22.04:** `sudo add-apt-repository ppa:deadsnakes/python3.12 && sudo apt update && sudo apt install python3.12 python3.12-venv`
>
> **Git installieren:**
>
> - **Windows:** `winget install Git.Git` oder [git-scm.com](https://git-scm.com/download/win)
> - **Linux:** `sudo apt install git`
>
> **VSCode installieren:**
>
> **Alle Systeme:** [Install](https://code.visualstudio.com/download)
>
> **Ollama installieren:**
>
> - **Alle Systeme:** [ollama.com/download](https://ollama.com/download)

---

## 1. Repository klonen

```bash
git clone TODO
cd smolagents
```

---

## 2. Virtuelle Umgebung erstellen und aktivieren

```bash
# Virtuelle Umgebung erstellen – Windows (py-Launcher)
py -3.12 -m venv .venv

# Virtuelle Umgebung erstellen – Linux/macOS
python3.12 -m venv .venv

# Aktivieren – Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Aktivieren – Windows (CMD)
.venv\Scripts\activate.bat

# Aktivieren – macOS/Linux
source .venv/bin/activate
```

> **Hinweis (Windows/PowerShell):** Falls du den Fehler `Skripts können nicht ausgeführt werden` siehst, führe einmalig aus:
>
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
>
> **Hinweis (Linux/Ubuntu):** Falls `python3.12 -m venv` mit `No module named venv` scheitert:
>
> ```bash
> sudo apt install python3.12-venv
> ```

---

## 3. Abhängigkeiten installieren

### Option A — Paketliste (für alle Features inkl. Notebook)

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Option B — Nur die Kern-App (ohne Notebook-Features)

```bash
python -m pip install --upgrade pip
pip install -e .
```

> `requirements.txt` enthält alle Pakete inkl. der Notebook-Abhängigkeiten (LangChain, FAISS, Datasets usw.).
> `pyproject.toml` enthält nur die Kern-App-Abhängigkeiten.

---

## 4. Konfiguration — `.env`-Datei anlegen

Erstelle eine Datei namens `.env` im Projektordner (neben `main.py`):

```env
# Pflichtfeld – dein OpenRouter API-Key
OPENROUTER_API_KEY=dein_key_hier

# Optional – Modell-ID (Standard: google/gemma-4-26b-a4b-it)
# Alle Modelle: https://openrouter.ai/models
MODEL_ID=google/gemma-4-26b-a4b-it

# Optional – Anzahl der DuckDuckGo-Suchergebnisse (Standard: 5)
DDG_MAX_RESULTS=5

# Optional – öffentlichen Gradio-Link erzeugen (Standard: false)
GRADIO_SHARE=false
```

> **API-Key**
>
> **Im Kurs:** Ihr erhaltet einen key mit Giuthaben, über den ihr das gemma4 Model nutzen könnt. Einfach in die `.env`-Datei eintragen und loslegen.
>
> **für später:** Registriere dich kostenlos auf [openrouter.ai](https://openrouter.ai) → Profil → API Keys → Key erstellen. Viele Modelle haben ein kostenloses Kontingent.
>
> **Windows-Falle:** Erstelle die Datei nicht über den Explorer — Windows versteckt Dateiendungen und erzeugt `.env.txt` statt `.env`. Nutze stattdessen das Terminal:
>
> ```powershell
> New-Item .env   # PowerShell – dann in VS Code öffnen: code .env
> ```
>
> Oder in der UI von VSCode einfach eine neue Datei erstellen

---

## 5. App starten

```bash
python main.py
```

Oder über den Script-Einstiegspunkt — **nur nach `pip install -e .` (Option B in Schritt 3)**:

```bash
smolagents-app
```

Danach öffnet sich die Gradio-Oberfläche automatisch unter `http://127.0.0.1:7860` im Browser.

---

## 6. Projektstruktur verstehen

TODO: Ist das noch aktuell?

```
smolagents/
├── main.py          # Einstiegspunkt – orchestriert die vier Schritte
├── settings.py      # .env laden und validieren (Settings-Dataclass)
├── openrouter.py    # OpenRouter-Modell-Client erstellen
├── tools.py         # Werkzeuge für den Agenten (DuckDuckGo, MCP, eigene)
├── agent_builder.py # Modell + Werkzeuge → ToolCallingAgent
├── gradio_ui.py     # Gradio-Chat-Oberfläche starten
├── agents.ipynb     # Interaktives Lern-Notebook (6 Beispiele)
├── requirements.txt # Alle Abhängigkeiten inkl. Notebook
├── pyproject.toml   # Paket-Metadaten und Kern-Abhängigkeiten
└── .env             # Deine Konfiguration (nicht ins Git committen!)
```

---

## 7. Jupyter Notebook — `agents.ipynb`

Das Notebook `agents.ipynb` ist ein eigenständiges Lernmaterial und läuft unabhängig von der Hauptanwendung.

### 7.1 Voraussetzungen für das Notebook

- Alle Pakete aus `requirements.txt` müssen installiert sein (siehe Schritt 3).
- **Ollama ist Pflicht** — auch wenn du OpenRouter als LLM-Backend nutzt. Die RAG-Embeddings (Beispiel 2) werden immer lokal über Ollama berechnet, da OpenRouter keine Embeddings-API anbietet.
  - Ollama installieren: [ollama.com/download](https://ollama.com/download)
  - Embedding-Modell herunterladen (immer nötig): `ollama pull nomic-embed-text`
  - LLM herunterladen (nur für Ollama-Backend): `ollama pull gemma4:e4b` (oder ein anderes Modell)
  - Ollama im Hintergrund laufen lassen (startet automatisch nach Installation)
- Für das **OpenRouter-Backend**: API-Key wie oben beschrieben.

### 7.2 Notebook in VS Code öffnen

> **Erweiterungen:** VS Code benötigt die Extensions **Python** (`ms-python.python`) und **Jupyter** (`ms-toolsai.jupyter`). Beim ersten Öffnen einer `.ipynb`-Datei erscheint automatisch ein Installations-Hinweis — einfach bestätigen.

1. Datei `agents.ipynb` im Explorer anklicken — VS Code öffnet sie als Notebook.
2. Oben rechts den Kernel auswählen: **`.venv (Python 3.12)`**
3. Falls kein Kernel erscheint: `Strg+Shift+P` → `Python: Select Interpreter` → `.venv` auswählen.
4. Falls der Kernel trotzdem fehlt: `pip install ipykernel` im aktivierten venv ausführen.

### 7.3 Notebook in Jupyter Lab / klassischem Jupyter öffnen

```bash
# Jupyter Lab installieren (einmalig)
pip install jupyterlab

# Starten
jupyter lab
```

Im Browser öffnet sich Jupyter Lab — `agents.ipynb` dort öffnen.

### 7.4 Konfiguration im Notebook

Im Notebook gibt es eine Konfigurationszelle (Zelle 2 — `⚙️ Konfiguration`). Dort kannst du:

- Das **Backend** wählen: `"ollama"` (lokal) oder `"openrouter"` (Cloud).
- Das Modell und die API-Endpunkte anpassen.

Alternativ kannst du eine `.env`-Datei im Projektordner anlegen — das Notebook liest sie automatisch:

```env
# ── Backend-Auswahl ──────────────────────────────────────────────
# "openrouter" = Cloud-API über OpenRouter (braucht OPENROUTER_API_KEY)
# "ollama"     = Lokales Modell via Ollama (kein API-Key nötig)
LLM_BACKEND=ollama

# ── OpenRouter-Einstellungen ─────────────────────────────────────
# API Key von https://openrouter.ai (nur nötig bei LLM_BACKEND=openrouter)
OPENROUTER_API_KEY=add_key_here

# Modell-ID für OpenRouter (siehe https://openrouter.ai/models)
OPENROUTER_MODEL_ID=google/gemma-4-26b-a4b-it

# ── Ollama-Einstellungen ─────────────────────────────────────────
# Modell-ID für Ollama (muss vorher mit "ollama pull" geladen werden)
OLLAMA_MODEL_ID=gemma4:e4b

# Ollama API-URL (Standard: http://localhost:11434/v1)
OLLAMA_API_BASE=http://localhost:11434/v1

# ── Allgemeine Einstellungen ─────────────────────────────────────
# DuckDuckGo search results limit (optional, defaults to 5)
DDG_MAX_RESULTS=5

# Whether to share the Gradio UI publicly (optional, defaults to False)
GRADIO_SHARE=false

# MCP-Tools via Docker Desktop aktivieren (optional, defaults to false)
# Docker Desktop muss laufen und "docker pull mcp/fetch" muss ausgeführt worden sein.
USE_DOCKER_MCP=false

```

### 7.5 Zellen der Reihe nach ausführen

Das Notebook ist in Abschnitte gegliedert — **Zellen immer von oben nach unten ausführen**, da spätere Zellen auf Variablen aus früheren aufbauen:

| Zelle            | Inhalt                                                                         |
| ---------------- | ------------------------------------------------------------------------------ |
| **Zelle 1**      | Pakete installieren / prüfen (progressiver Fortschrittsbalken)                 |
| **Zelle 2**      | Backend wählen und Konfiguration laden                                         |
| **Zelle 3**      | Modell initialisieren und Verbindung testen                                    |
| **Zelle 4**      | Beispiel 1: Web-Such-Agent mit DuckDuckGo                                      |
| **Zellen 5–9**   | Beispiel 2: RAG — Wissensbasis laden, Vektordatenbank aufbauen, Retriever-Tool |
| **Zelle 10**     | Beispiel 3: Code-Debugging mit CodeAgent                                       |
| **Zellen 11–12** | Beispiel 4: Eigene Tools mit `@tool`-Decorator                                 |
| **Zellen 13**    | Beispiel 5: Multi-Agenten-System                                               |
| **Zelle 14**     | Beispiel 6 (Bonus): Gradio-Chat-Oberfläche                                     |

> **Tipp:** Zelle 1 (Paketinstallation) kann beim ersten Ausführen einige Minuten dauern. Danach empfiehlt sich ein Kernel-Neustart (`Kernel` → `Restart Kernel`) bevor du weitermachst.

---

## 8. Optionale Features freischalten

### Tools aktivieren (DuckDuckGo + MCP)

Standardmäßig startet der Agent ohne Werkzeuge (`tools=[]`). Um die vorkonfigurierten Tools zu aktivieren, öffne `agent_builder.py` und tausche die aktive Zeile:

```python
# Diese Zeile auskommentieren:
# return ToolCallingAgent(tools=[], model=model, stream_outputs=True)

# Diese Zeile einkommentieren:
return ToolCallingAgent(tools=get_tools(settings), model=model, stream_outputs=True)
```

### MCP-Tools (Docker-basiert)

`tools.py` enthält einen vorbereiteten MCP-Server (`mcp/fetch`), der Docker Desktop benötigt:

- Docker Desktop installieren und starten.
- Das Docker-Image wird beim ersten Start automatisch geladen.
- Gibt dem Agenten die Fähigkeit, beliebige URLs abzurufen.

Weitere MCP-Server findest du im [Docker MCP Catalog](https://hub.docker.com/catalogs/mcp).

### Anderes Modell verwenden

Ändere `MODEL_ID` in deiner `.env`-Datei. Alle verfügbaren Modelle auf OpenRouter: [openrouter.ai/models](https://openrouter.ai/models).

Für kostenlose Modelle empfehlen sich z. B.:

- `nvidia/nemotron-3-super-120b-a12b:free`
- `google/gemma-4-26b-a4b-it:free`
- `openai/gpt-oss-120b:free`
- `qwen/qwen3-coder:free`

---

## 9. Häufige Fehler

| Fehler                                             | Ursache                                   | Lösung                                                                                |
| -------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------- |
| `Missing OPENROUTER_API_KEY`                       | `.env`-Datei fehlt oder Key nicht gesetzt | `.env`-Datei anlegen, Key eintragen                                                   |
| `.env` nicht gefunden / Key trotzdem leer          | Windows hat `.env.txt` erzeugt            | Dateiendungen einblenden und Datei zu `.env` umbenennen                               |
| `ModuleNotFoundError: No module named 'mcp'`       | `mcp`-Paket nicht installiert             | `pip install mcp` oder `pip install -r requirements.txt`                              |
| `ModuleNotFoundError: No module named 'ipykernel'` | `ipykernel` nicht installiert             | `pip install ipykernel` im aktivierten venv                                           |
| `python: command not found` (Linux)                | `python` existiert nicht, nur `python3`   | Venv mit `python3.12 -m venv .venv` erstellen; nach Aktivierung funktioniert `python` |
| `No module named venv` (Linux)                     | `python3.12-venv` fehlt                   | `sudo apt install python3.12-venv`                                                    |
| `smolagents-app: command not found`                | Paket nicht als editable installiert      | `pip install -e .` ausführen                                                          |
| `Connection refused` (Ollama)                      | Ollama läuft nicht                        | Ollama starten oder `ollama serve` ausführen                                          |
| `Kernel not found` (Notebook)                      | VS Code findet das `.venv` nicht          | Interpreter manuell auswählen: `Strg+Shift+P` → `Python: Select Interpreter`          |
| Gradio öffnet sich nicht                           | Port 7860 belegt                          | `netstat -ano \| findstr 7860` (Windows) oder `lsof -i :7860` (Linux/Mac)             |
| `Scripts cannot be loaded` (PowerShell)            | ExecutionPolicy zu restriktiv             | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`                |

---

## 10. Deinstallation / Aufräumen

```bash
# Virtuelle Umgebung löschen
rm -rf .venv          # macOS/Linux
Remove-Item -Recurse -Force .venv  # Windows PowerShell
```

Die `.env`-Datei enthält deinen API-Key — stelle sicher, dass sie **nicht in Git committed** wird. Überprüfe die `.gitignore`.
