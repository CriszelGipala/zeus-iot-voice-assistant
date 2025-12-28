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
    Optional extension: call a remote LLM API.
    If not configured, return a fallback None.
    """
    if not AI_API_URL or not AI_API_KEY:
        return None

    try:
        # Import requests lazily to avoid hard dependency when offline
        import requests  # type: ignore
        r = requests.post(
            AI_API_URL,
            headers={"Authorization": f"Bearer {AI_API_KEY}"},
            json={"prompt": question},
        )
        if r.status_code != 200:
            return None
        data = r.json()
        # This depends on the API provider
        return str(data.get("text", "")).strip() or None
    except Exception:
        return None

def ai_fallback_response() -> str:
    return random.choice(FALLBACK_RESPONSE)