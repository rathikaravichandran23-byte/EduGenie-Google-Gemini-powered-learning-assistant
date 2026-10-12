import os
from functools import lru_cache
from dotenv import load_dotenv
load_dotenv()

class GeminiConfigurationError(RuntimeError):
    pass

@lru_cache(maxsize=1)
def _client():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key or key == "your_gemini_api_key_here":
        raise GeminiConfigurationError("Gemini API key missing. Add GEMINI_API_KEY to your .env file.")
    from google import genai
    return genai.Client(api_key=key)

def generate_text(prompt: str) -> str:
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    response = _client().models.generate_content(model=model, contents=prompt)
    text = getattr(response, "text", None)
    if not text or not text.strip():
        raise RuntimeError("Gemini returned an empty response. Please try again.")
    return text.strip()
