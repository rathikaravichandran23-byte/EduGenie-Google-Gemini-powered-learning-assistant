from gemini_client import generate_text

def answer_question(question: str) -> str:
    return generate_text(
        "You are EduGenie, a careful educational assistant. Answer accurately in simple, "
        "clear language, using examples where useful. Admit uncertainty when needed.\nQuestion: "
        + question
    )
