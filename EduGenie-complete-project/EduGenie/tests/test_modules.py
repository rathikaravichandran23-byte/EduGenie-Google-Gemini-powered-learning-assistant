import json
import pytest
import quiz_module

def test_quiz_parser_valid_json():
    data = {"questions":[{"question":f"Q{i}?","options":["a","b","c","d"],"answer":"a"} for i in range(3)]}
    result = quiz_module._extract_json(json.dumps(data))
    assert len(result["questions"]) == 3
    assert len(result["questions"][0]["options"]) == 4

def test_quiz_parser_markdown_fence():
    raw = '```json\n' + json.dumps({"questions":[{"question":f"Q{i}?","options":["a","b","c","d"],"answer":"a"} for i in range(3)]}) + '\n```'
    assert len(quiz_module._extract_json(raw)["questions"]) == 3

def test_quiz_parser_rejects_wrong_count():
    with pytest.raises(ValueError):
        quiz_module._extract_json('{"questions": []}')

def test_quiz_generation_uses_generator(monkeypatch):
    raw = json.dumps({"questions":[{"question":f"Q{i}?","options":["a","b","c","d"],"answer":"a"} for i in range(3)]})
    monkeypatch.setattr(quiz_module, "generate_text", lambda prompt: raw)
    assert len(quiz_module.generate_quiz("study notes")["questions"]) == 3
