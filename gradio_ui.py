# -----------------------------------------------------------------------------
# gradio_ui.py – eine Web-Oberfläche für den Agenten starten
#
# Gradio ist eine Python-Bibliothek, mit der ihr in wenigen Zeilen
# eine interaktive Web-App für eure KI-Modelle bauen könnt.
# smolagents bringt eine fertige GradioUI-Klasse mit, die einen Chat-Interface
# inklusive Tool-Calls, Zwischenschritte und Streaming bietet.
# Das Beste: Ihr braucht kein HTML, kein JavaScript, kein CSS.
# Einfach Python – und schon habt ihr eine Demo, die ihr im Browser öffnen
# oder mit einem öffentlichen Link (gradio_share=True) teilen könnt.
# -----------------------------------------------------------------------------

from __future__ import annotations

from smolagents import GradioUI, ToolCallingAgent

from settings import Settings


# launch_gradio() – startet den lokalen Web-Server mit der Chat-Oberfläche.
#
# Was passiert im Detail?
#   - GradioUI(agent) wickelt den Agenten in eine fertige Chat-Komponente.
#   - reset_agent_memory=False bedeutet, der Agent merkt sich den
#     bisherigen Gesprächsverlauf innerhalb einer Session.
#     Das ist wichtig für natürliche Mehrrundenkonversationen.
#   - gradio_share=True erzeugt einen temporären öffentlichen Link
#     über die Gradio-Infrastruktur – praktisch zum Vorführen oder Testen
#     auf einem fremden Gerät, ohne Firewall-Probleme.
#
# Nach dem Start seht ihr im Terminal eine lokale URL (z. B. http://127.0.0.1:7860).
# Öffnet sie im Browser und ihr könnt direkt mit eurem Agenten chatten!
def launch_gradio(agent: ToolCallingAgent, settings: Settings) -> None:
    ui = GradioUI(agent, reset_agent_memory=False)

    ui.launch(share=settings.gradio_share)
