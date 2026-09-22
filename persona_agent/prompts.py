from pypdf import PdfReader

from persona_agent.config import LINKEDIN_PDF_PATH, SUMMARY_PATH, SYSTEM_PROMPT_PATH


def load_text(path) -> str:
    return path.read_text(encoding="utf-8")


def load_linkedin_profile(path=LINKEDIN_PDF_PATH) -> str:
    reader = PdfReader(path)
    pages = []
    for page in reader.pages:
        content = page.extract_text()
        if content:
            pages.append(content)
    return "".join(pages)


def build_system_prompt() -> str:
    summary = load_text(SUMMARY_PATH)
    linkedin_data = load_linkedin_profile()
    system_prompt = load_text(SYSTEM_PROMPT_PATH)
    return system_prompt.replace("{summary}", summary).replace("{linkedin}", linkedin_data)
