from openai import OpenAI

from persona_agent.config import GEMINI_BASE_URL, GOOGLE_API_KEY, MODEL_NAME
from persona_agent.prompts import build_system_prompt
from persona_agent.tools import TOOLS, handle_tool_calls


class PersonaAgent:
    def __init__(self):
        self.client = OpenAI(api_key=GOOGLE_API_KEY, base_url=GEMINI_BASE_URL)
        self.system_prompt = build_system_prompt()

    def chat(self, message, history):
        messages = (
            [{"role": "system", "content": self.system_prompt}]
            + history
            + [{"role": "user", "content": message}]
        )
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
        )
        while response.choices[0].finish_reason == "tool_calls":
            assistant_message = response.choices[0].message
            results = handle_tool_calls(assistant_message.tool_calls)
            messages.append(assistant_message)
            messages.extend(results)
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=TOOLS,
            )
        return response.choices[0].message.content
