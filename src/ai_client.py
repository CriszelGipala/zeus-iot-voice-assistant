import random

# Built-in fallback lines used when cloud AI is not configured.
FALLBACK_RESPONSE = [
    "So sorry — my smart assistant is offline right now.",
    "I can help with the basics: time, temperature, and humidity.",
    "You can ask: “What’s the temperature?” or “What’s the time?”",
    "If the internet comes back, I can answer more questions.",
]

def ask_ai(_question: str) -> None:
    """
    Placeholder for cloud AI. Not enabled in this project.
    Returning None tells callers to use the fallback response.
    """
    return None

def ai_fallback_response() -> str:
    """Return a friendly built-in response when AI is unavailable."""
    return random.choice(FALLBACK_RESPONSE)


