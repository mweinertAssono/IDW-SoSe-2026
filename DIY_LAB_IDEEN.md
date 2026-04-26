# DIY Lab – Projektideen für Tag 2

Baut heute etwas, das ihr nächste Woche noch benutzt.  
Die folgenden Ideen sind Ausgangspunkte – anpassen, erweitern, umbauen ist ausdrücklich erwünscht.

---

## 1. Persönlicher Lern-Assistent mit Karteikarten-Export

**Was es macht:** Der Agent liest Lernmaterial (PDF, URL oder eingefügter Text), fasst die wichtigsten Konzepte zusammen und exportiert sie direkt als Anki-kompatibles `.apkg` oder als CSV für Quizlet.

**Warum sinnvoll:** Wer regelmäßig lernt (Sprachen, Zertifizierungen, Studium) spart stundenlange manuelle Arbeit. Statt Karteikarten abtippen – einmal URL rein, fertig.

**Kernwerkzeuge:**

- `VisitWebpageTool` / Datei-Upload zum Lesen von Quellen
- Eigenes Tool zum Schreiben der `.csv`- oder `.apkg`-Datei
- Optional: Wikipedia-Tool für Kontext-Anreicherung

---

## 2. Meeting-Nachbereitung & Aufgaben-Extraktion

**Was es macht:** Transkript (z. B. aus Teams oder Zoom) wird eingefügt oder hochgeladen. Der Agent extrahiert To-dos mit Verantwortlichkeiten, fasst Entscheidungen zusammen und schreibt optional ein strukturiertes Protokoll ins gewünschte Format (Markdown, Confluence-Seite, E-Mail-Entwurf).

**Warum sinnvoll:** Nach jedem Meeting dasselbe manuelle Protokollieren entfällt. Besonders nützlich für Scrum-Teams, die viele kurze Meetings haben.

**Kernwerkzeuge:**

- Eigenes Tool zum Lesen von `.txt`/`.vtt`-Transkripten
- Optional: HTTP-Tool für Confluence- oder Notion-API
- `UserInputTool` für interaktive Rückfragen ("Wer ist für Task X verantwortlich?")

---

## 3. Bewerbungshelfer – Stellenanzeige trifft Lebenslauf

**Was es macht:** Der Agent liest eine Stellenanzeige (URL oder Text) und den eigenen Lebenslauf. Er analysiert die Lücken, formuliert ein passendes Anschreiben und gibt konkrete Hinweise, welche Skills im CV besser hervorgehoben werden sollten.

**Warum sinnvoll:** Bewerbungsphase ist zeitintensiv und emotional belastend. Ein Agent, der sachlich vergleicht und Texte vorschlägt, nimmt viel Reibung raus.

**Kernwerkzeuge:**

- `VisitWebpageTool` für Stellenanzeigen
- Datei-Tool zum Lesen des Lebenslaufs (`.txt` / Markdown)
- Eigenes Tool zum Speichern des generierten Anschreibens

---

## 4. Code-Review-Assistent für eigene Projekte

**Was es macht:** Der Agent liest Quellcode aus einem lokalen Verzeichnis oder GitHub-Repository, prüft auf häufige Probleme (z. B. Sicherheitslücken nach OWASP, fehlende Tests, schlechte Benennung) und liefert priorisierte, kommentierte Review-Kommentare – genau wie ein erfahrener Kollege im PR.

**Warum sinnvoll:** Solo-Entwickler und kleine Teams haben selten die Zeit für tiefgehende Reviews. Ein Agent, der 80 % der offensichtlichen Probleme findet, ist ein echter Mehrwert im Alltag.

**Kernwerkzeuge:**

- `PythonInterpreterTool` zum Lesen und Analysieren von Dateien
- Optional: GitHub-API-Tool zum direkten Kommentieren von Pull Requests
- `DuckDuckGoSearchTool` zum Nachschlagen von Best Practices

---

## 5. Persönlicher Finanz-Tracker & Spar-Coach

**Was es macht:** Der Agent liest exportierte Kontoauszüge (CSV von der Bank), kategorisiert Ausgaben automatisch, erkennt Muster ("Du gibst jeden Monat ~80 € für Lieferdienste aus") und schlägt konkrete Einsparpotenziale vor – ohne dass Daten je eine eigene API verlassen.

**Warum sinnvoll:** Finanz-Apps senden Daten in die Cloud. Dieser Agent läuft vollständig lokal – volle Datenkontrolle, persönlicher Mehrwert, technisch spannend.

**Kernwerkzeuge:**

- `PythonInterpreterTool` mit `pandas`/`csv` für Datenanalyse
- Eigenes Tool zum Einlesen und Normalisieren von Bank-CSVs
- Optional: Tool zum Erstellen von Diagrammen (matplotlib) und Exportieren als PNG

---
