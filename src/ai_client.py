import os
import random
from config import AI_API_URL, AI_API_KEY

FALLBACK_RESPONSE = [
    "Sorry, my smart assistant is offline right now.",
    "I can only help with: time, temperature, humidity right now.",
    "Try saying: what time is it?",
    "If the internet returns, I can answer more questions."
]

def ask_ai(question: str) -> str | None:
    """
    Call a remote LLM API. If unavailable or errors, return None to trigger fallback.
    """
    if not AI_API_KEY:
        return None  # No key configured

    # Default to OpenAI Chat Completions if no custom URL provided
    url = (AI_API_URL or "").strip() or "https://api.openai.com/v1/chat/completions"
    is_openai = "openai.com" in url or url.endswith("/chat/completions")

    try:
        import requests  # type: ignore  # imported lazily

        headers = {"Authorization": f"Bearer {AI_API_KEY}"}
        json_payload = None

        if is_openai:
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            json_payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are Zeus, an IoT voice assistant on a Raspberry Pi."},
                    {"role": "user", "content": question},
                ],
                "temperature": 0.7,
                "max_tokens": 200,
            }
        else:
            # Generic JSON payload for custom endpoints expecting {'prompt': ...}
            json_payload = {"prompt": question}

        r = requests.post(url, headers=headers, json=json_payload, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()

        if is_openai:
            # OpenAI Chat Completions shape
            choices = data.get("choices") or []
            if not choices:
                return None
            message = choices[0].get("message") or {}
            content = (message.get("content") or "").strip()
            return content or None
        else:
            # Generic provider: expect {'text': '...'}
            return str(data.get("text", "")).strip() or None
    except Exception:
        return None

def ai_fallback_response() -> str:
    return random.choice(FALLBACK_RESPONSE)