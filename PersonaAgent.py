import os
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio

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

# define chat function
def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": systemPrompt}] + history + [{"role": "user", "content": message}]
    response = google.chat.completions.create(model="gemini-3.5-flash-lite", messages = messages)
    return response.choices[0].message.content

# chat UI with gradio
gradio.ChatInterface(chat).launch(inbrowser=True)