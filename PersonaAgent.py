import os
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio
import json
import requests

# load or reload env
load_dotenv(override=True)

# read keys
google_api_key = os.getenv('GOOGLE_API_KEY')
pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")

# push notifications Base URL
pushover_url = "https://api.pushover.net/1/messages.json"

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
# email tool
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

# push notification tool
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {"type": "string", "description": "Any additional info about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

# create tools object
tools = [
    {
        "type": "function",
        "function": recordEmailJson
    },
    {
        "type": "function", 
        "function": record_user_details_json
    },
    {
        "type": "function", 
        "function": record_unknown_question_json
    }
]

# define email function
def record_email_tool(email):
    print(f"Tool called to record an email: {email}")
    with open("data/email.txt", "a", encoding="utf-8") as f:
        f.write(email + "\n")
    return "Email received"

def push(message):
    print(f"Push: {message}")
    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    requests.post(pushover_url, data=payload)

# define - record user details
def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return "OK"

# define - record unknown questions
def record_unknown_question(question):
    push(f"Recording {question} asked that I couldn't answer")
    return "OK"

# tackle tools
def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else "No tool found"
        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return results

# define chat function
def chat(message, history):
    messages = [{"role": "system", "content": systemPrompt}] + history + [{"role": "user", "content": message}]
    response = google.chat.completions.create(model="gemini-3.5-flash-lite", messages = messages, tools= tools)
    while response.choices[0].finish_reason=="tool_calls":
        message = response.choices[0].message
        tool_calls = message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(message)
        messages.extend(results)
        response = google.chat.completions.create(model="gemini-3.5-flash-lite", messages=messages, tools=tools)
    return response.choices[0].message.content

# chat UI with gradio
gradio.ChatInterface(chat).launch(inbrowser=True)