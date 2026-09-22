import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")

PUSHOVER_URL = "https://api.pushover.net/1/messages.json"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL_NAME = "gemini-3.5-flash-lite"

SUMMARY_PATH = DATA_DIR / "Summary.txt"
SYSTEM_PROMPT_PATH = DATA_DIR / "SystemPrompt.txt"
LINKEDIN_PDF_PATH = DATA_DIR / "Profile.pdf"
EMAIL_LOG_PATH = DATA_DIR / "email.txt"
