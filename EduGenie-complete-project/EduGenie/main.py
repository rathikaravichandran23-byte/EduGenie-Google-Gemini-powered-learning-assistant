from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
app = FastAPI(title="EduGenie", version="1.0.0")
app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")
templates = Jinja2Templates(directory=str(ROOT / "templates"))

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)
class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)
class TopicRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000)
    level: str = Field(default="Beginner", max_length=100)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok", "app": "EduGenie"}

@app.post("/qa")
async def qa(data: QuestionRequest):
    try: return {"result": answer_question(data.question.strip())}
    except Exception as exc: raise HTTPException(status_code=502, detail=str(exc)) from exc

@app.post("/explain")
async def explain(data: TopicRequest):
    try: return {"result": explain_topic(data.topic.strip(), data.level)}
    except Exception as exc: raise HTTPException(status_code=502, detail=str(exc)) from exc

@app.post("/quiz")
async def quiz(data: TextRequest):
    try: return {"result": generate_quiz(data.text.strip())}
    except Exception as exc: raise HTTPException(status_code=502, detail=str(exc)) from exc

@app.post("/summarize")
async def summarize(data: TextRequest):
    try: return {"result": summarize_text(data.text.strip())}
    except Exception as exc: raise HTTPException(status_code=502, detail=str(exc)) from exc

@app.post("/learn/recommendations")
async def recommendations(data: TopicRequest):
    try: return {"result": get_learning_recommendations(data.topic.strip(), data.level)}
    except Exception as exc: raise HTTPException(status_code=502, detail=str(exc)) from exc
