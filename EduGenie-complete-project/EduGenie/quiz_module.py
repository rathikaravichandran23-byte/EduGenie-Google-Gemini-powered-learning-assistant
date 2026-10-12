import json, re
from gemini_client import generate_text

def _extract_json(text: str) -> dict:
    text = re.sub(r"^\s*```(?:json)?\s*", "", text.strip(), flags=re.I)
    text = re.sub(r"\s*```\s*$", "", text)
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start: text = text[start:end+1]
    data = json.loads(text)
    questions = data.get("questions") if isinstance(data, dict) else data
    if not isinstance(questions, list) or len(questions) != 3:
        raise ValueError("Quiz must contain exactly 3 questions.")
    result = []
    for item in questions:
        options = item.get("options", [])
        answer = item.get("answer", item.get("correct_answer", ""))
        if not isinstance(options, list) or len(options) != 4:
            raise ValueError("Each question must have exactly 4 options.")
        if isinstance(answer, int) and 0 <= answer < 4: answer = options[answer]
        if isinstance(answer, str) and answer.strip().upper() in {"A","B","C","D"} and answer not in options:
            answer = options[ord(answer.strip().upper()) - ord("A")]
        if answer not in options: raise ValueError("Correct answer must match an option.")
        question = str(item.get("question", "")).strip()
        if not question: raise ValueError("Question cannot be empty.")
        result.append({"question": question, "options": [str(x) for x in options],
                       "answer": answer, "explanation": str(item.get("explanation", "")).strip()})
    return {"questions": result}

def generate_quiz(text: str) -> dict:
    prompt = ('Create exactly 3 MCQs based only on this study text. Each has exactly 4 options, '
              'one correct answer matching the option text, and a brief explanation. Return only JSON: '
              '{"questions":[{"question":"...","options":["...","...","...","..."],'
              '"answer":"exact option text","explanation":"..."}]}\nTEXT:\n' + text)
    try: return _extract_json(generate_text(prompt))
    except (ValueError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not parse quiz response; please try again. Details: {exc}") from exc
