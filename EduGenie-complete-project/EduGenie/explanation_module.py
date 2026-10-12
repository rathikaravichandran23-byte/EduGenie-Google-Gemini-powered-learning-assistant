import os
from functools import lru_cache
from gemini_client import generate_text

@lru_cache(maxsize=1)
def _local_pipeline():
    from transformers import pipeline
    model = os.getenv("LOCAL_EXPLAINER_MODEL", "MBZUAI/LaMini-Flan-T5-783M")
    return pipeline("text2text-generation", model=model, device=-1)

def explain_topic(topic: str, level: str = "Beginner") -> str:
    if os.getenv("ENABLE_LOCAL_EXPLAINER", "false").lower() in {"1", "true", "yes"}:
        try:
            output = _local_pipeline()(
                f"Explain {topic} to a {level} learner with simple language and one example.",
                max_new_tokens=220, do_sample=False
            )
            if output and output[0].get("generated_text", "").strip():
                return output[0]["generated_text"].strip()
        except Exception:
            pass
    return generate_text(
        f"Explain {topic} to a {level} learner in plain language. Include an analogy, "
        "one example, and a short recap. Avoid unexplained jargon."
    )
