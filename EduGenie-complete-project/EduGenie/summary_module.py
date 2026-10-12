from gemini_client import generate_text

def summarize_text(text: str) -> str:
    return generate_text("Summarize this educational text for revision. Keep important facts, "
                         "definitions, and relationships. Use concise bullet points and do not "
                         "add unsupported claims.\nTEXT:\n" + text)
