import json

import requests

from persona_agent.config import EMAIL_LOG_PATH, PUSHOVER_TOKEN, PUSHOVER_URL, PUSHOVER_USER

RECORD_EMAIL_SCHEMA = {
    "name": "record_email_tool",
    "description": "Use this tool to record that a user provided their email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of the user",
            }
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

RECORD_USER_DETAILS_SCHEMA = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {
                "type": "string",
                "description": "Any additional info about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

RECORD_UNKNOWN_QUESTION_SCHEMA = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered",
            },
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

TOOLS = [
    {"type": "function", "function": RECORD_EMAIL_SCHEMA},
    {"type": "function", "function": RECORD_USER_DETAILS_SCHEMA},
    {"type": "function", "function": RECORD_UNKNOWN_QUESTION_SCHEMA},
]


def record_email_tool(email):
    print(f"Tool called to record an email: {email}")
    with open(EMAIL_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(email + "\n")
    return "Email received"


def push(message):
    print(f"Push: {message}")
    payload = {"user": PUSHOVER_USER, "token": PUSHOVER_TOKEN, "message": message}
    requests.post(PUSHOVER_URL, data=payload)


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return "OK"


def record_unknown_question(question):
    push(f"Recording {question} asked that I couldn't answer")
    return "OK"


TOOL_HANDLERS = {
    "record_email_tool": record_email_tool,
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}


def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        handler = TOOL_HANDLERS.get(tool_name)
        result = handler(**arguments) if handler else "No tool found"
        results.append(
            {
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id,
            }
        )
    return results
