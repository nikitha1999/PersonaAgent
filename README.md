# PersonaAgent
PersonaAgent is an AI-powered digital twin of Nikitha that represents her professional experience, technical skills, projects, and career journey, enabling users to interact with her professional profile in an immersive and personalized way.

## 🎥 Demo
https://github.com/user-attachments/assets/9281e20d-0211-48a8-b9eb-c94317be5c3e

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with:

```
GOOGLE_API_KEY=...
PUSHOVER_USER=...
PUSHOVER_TOKEN=...
```

Place persona files in `data/`:
- `Summary.txt`
- `SystemPrompt.txt`
- `Profile.pdf`

## Run
```bash
python main.py
```

Or as a module:

```bash
python -m persona_agent
```
