from pathlib import Path

import gradio as gr

from persona_agent.agent import PersonaAgent
from persona_agent.theme import PERSONA_THEME

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
STYLES_PATH = ASSETS_DIR / "styles.css"
BOT_AVATAR = ASSETS_DIR / "bot-avatar.svg"

HEADER_HTML = """
<div class="persona-hero">
  <div class="persona-mark" aria-hidden="true">N</div>
  <div class="persona-copy">
    <p class="persona-kicker">Digital twin</p>
    <h1>Nikitha</h1>
    <p class="persona-role">Software Engineer · Career, Skills, and Projects</p>
  </div>
</div>
"""

FOOTER_HTML = """
<p class="persona-footnote">
  An AI representation of Nikitha’s professional profile. For opportunities, leave your email in chat.
</p>
"""

EXAMPLES = [
    "What is Nikitha's professional background?",
    "Which technologies and skills does she work with?",
    "Is she open to new opportunities?",
    "How can I get in touch?",
]


def build_interface(chat_fn):
    with gr.Blocks(title="Nikitha · Digital Twin", fill_height=True, fill_width=False) as demo:
        gr.HTML(HEADER_HTML)
        gr.ChatInterface(
            fn=chat_fn,
            chatbot=gr.Chatbot(
                show_label=False,
                height="62vh",
                layout="bubble",
                placeholder=(
                    "<div class='chat-placeholder'><strong>Welcome.</strong>"
                    "Ask about experience, skills, projects, or how to get in touch.</div>"
                ),
                avatar_images=(None, str(BOT_AVATAR)),
                buttons=["copy"],
                elem_classes=["persona-chat"],
            ),
            textbox=gr.Textbox(
                placeholder="Ask about experience, skills, or projects…",
                container=False,
                scale=7,
                submit_btn=True,
                autofocus=True,
            ),
            examples=EXAMPLES,
            example_labels=["Background", "Skills", "Opportunities", "Contact"],
            flagging_mode="never",
            fill_height=True,
        )
        gr.HTML(FOOTER_HTML)
    return demo


def main():
    agent = PersonaAgent()
    demo = build_interface(agent.chat)
    demo.launch(
        inbrowser=True,
        theme=PERSONA_THEME,
        css_paths=str(STYLES_PATH),
        footer_links=[],
        allowed_paths=[str(ASSETS_DIR)],
    )


if __name__ == "__main__":
    main()
