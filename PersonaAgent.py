import os
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio
import json

# load or reload env
load_dotenv(override=True)

# read keys
google_api_key = os.getenv('GOOGLE_API_KEY')

# google Gemini Base URL
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

# AI model deifinition
google = OpenAI(api_key=google_api_key, base_url=gemini_url)

# read summary from data
summary = ""
with open("data/Summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

# read linkedin profile from data
linkedinData = ""
reader = PdfReader("data/Profile.pdf")
for page in reader.pages:
    pageContent = page.extract_text()
    if pageContent:
        linkedinData += pageContent

# read System Role Prompt
systemPrompt = ""
with open("data/SystemPrompt.txt", "r", encoding="utf-8") as f:
    systemPrompt = f.read()

# add summary and linkedin data to system prompt
systemPrompt = systemPrompt.replace("{summary}", summary)
systemPrompt = systemPrompt.replace("{linkedin}", linkedinData)

# write tools
# as of now only email is the tool
recordEmailJson = {
    "name": "record_email_tool",
    "description": "Use this tool to record that a user provided their email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of the user"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

# create tools object
tools = [
    {
        "type": "function",
        "function": recordEmailJson
    }
]

# define email function
def record_email_tool(email):
    print(f"Tool called to record an email: {email}")
    with open("data/email.txt", "a", encoding="utf-8") as f:
        f.write(email + "\n")
    return "Email received"

# define chat function
def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": systemPrompt}] + history + [{"role": "user", "content": message}]
    response = google.chat.completions.create(model="gemini-3.5-flash-lite", messages = messages, tools= tools)

    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        messages.append(message)
        for tool_call in message.tool_calls:
            email = json.loads(tool_call.function.arguments).get("email")
            record_email_tool(email)
            messages.append({"role": "tool", "content": "Email recorded", "tool_call_id": tool_call.id})
        response = google.chat.completions.create(model="gemini-3.5-flash-lite", messages=messages, tools=tools)
    return response.choices[0].message.content

# chat UI with gradio
gradio.ChatInterface(chat).launch(inbrowser=True)