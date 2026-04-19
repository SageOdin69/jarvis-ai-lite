import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:1b"

SYSTEM_PROMPT = """
You are Jarvis, a real AI assistant running on a local machine.

Rules:
- You do NOT have real-world experiences.
- You do NOT travel or have a physical body.
- Do NOT make up stories.
- Be honest and grounded.
"""

def ask_ai(messages):
    payload = {
        "model": MODEL_NAME,
        "messages": messages, #[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["message"]["content"]