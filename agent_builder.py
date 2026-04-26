# -----------------------------------------------------------------------------
# agent_builder.py – den KI-Agenten zusammenbauen
#
# Hier passiert die eigentliche Magie: Wir verbinden das Sprachmodell
# mit den Werkzeugen zu einem handlungsfähigen Agenten.
# Ein "ToolCallingAgent" ist ein Agent, der:
#   1. Die Nutzeranfrage analysiert.
#   2. Selbstständig entscheidet, welche Werkzeuge er nutzen möchte.
#   3. Die Werkzeuge aufruft, die Ergebnisse verarbeitet.
#   4. Diesen Zyklus wiederholt, bis er eine fertige Antwort hat.
# Dieses Muster nennt sich "ReAct" (Reason + Act) und ist eines der
# fundamentalen Konzepte moderner LLM-Agenten.
# -----------------------------------------------------------------------------

from datetime import datetime

from smolagents import CodeAgent, ToolCallingAgent
from smolagents.memory import ActionStep, FinalAnswerStep
from smolagents.monitoring import LogLevel

from settings import Settings
from tools import get_tools


# build_agent() – Modell und Werkzeuge werden hier verheiratet.
#
# Parameter:
#   model   – der konfigurierte Modell-Client aus openrouter.py
#   settings – das Settings-Objekt, das an get_tools() weitergereicht wird
#
# stream=True bedeutet, dass die Antwort des Agenten Stück für Stück
# gestreamt wird, anstatt erst am Ende komplett zu erscheinen.
# Das verbessert die wahrgenommene Geschwindigkeit enorm –
# der Nutzer sieht sofort, dass etwas passiert.
#
# Der zurückgegebene Agent ist vollständig einsatzbereit.
# Ihr könnt ihn direkt per agent.run("Deine Frage") ansprechen –
# oder, wie wir es tun, in eine Gradio-Oberfläche einbetten.
def _log_step(step) -> None:
    """Gibt pro Schritt eine kompakte Zeile ins Terminal aus:
    z. B.  Step 1 → web_search
           Step 2 → final_answer ✓
    Alle anderen Details (Observations, Fehler, Payloads) bleiben verborgen."""
    if isinstance(step, ActionStep):
        tool_name = "(thinking)"
        if step.tool_calls:
            tool_name = step.tool_calls[0].name
        print(f"  Step {step.step_number} → {tool_name}")
    elif isinstance(step, FinalAnswerStep):
        print("  ✓ Fertig")


def build_agent(model: object, settings: Settings) -> ToolCallingAgent:
#    return ToolCallingAgent(tools=[], model=model, stream_outputs=True)
    today = datetime.now().strftime("%Y-%m-%d")
    return ToolCallingAgent(
        tools=get_tools(settings),
        model=model,
        instructions=f"Today's date is {today}.",
        max_steps=10,
        stream_outputs=True,
        verbosity_level=LogLevel.ERROR,
        step_callbacks=[_log_step],
    )
