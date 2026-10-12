from gemini_client import generate_text

def get_learning_recommendations(topic: str, level: str = "Beginner") -> str:
    return generate_text(
        f"Create a practical learning path for {topic} for a {level} learner. "
        "Organize foundations to advanced topics. Include an estimated timeline, practice tasks, "
        "checkpoints, and useful resource types. Do not invent URLs; suggest search terms instead."
    )
