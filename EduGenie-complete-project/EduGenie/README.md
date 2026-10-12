# EduGenie — Gemini-powered learning assistant

Based on the supplied PDF: FastAPI backend, HTML/CSS frontend, Q&A, simplified explanations, 3-question MCQ quizzes, summaries, and learning paths. The PDF proposes Gemini for Q&A/quiz/summary/learning paths and LaMini-Flan-T5 for local explanations. To keep the default install small, explanations use Gemini by default; local LaMini mode is optional.

## Windows + VS Code setup
1. Extract this ZIP.
2. In VS Code choose **File → Open Folder** and select the `EduGenie` folder containing `main.py` and `requirements.txt`.
3. Choose **Terminal → New Terminal**. Run `dir` and check that `main.py`, `requirements.txt`, `templates`, and `static` appear.
4. Create a virtual environment:
   ```powershell
   python -m venv .venv
   ```
5. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks scripts, select Command Prompt as terminal and run `.venv\Scripts\activate.bat`.
6. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```
7. Get a Gemini API key at https://aistudio.google.com/. Keep it private.
8. Copy `.env.example` to `.env` in the same folder as `main.py`:
   ```powershell
   Copy-Item .env.example .env
   ```
9. Open `.env`; replace `your_gemini_api_key_here` with your real key. Save the file. Keep `.env private.
10. Start the app:
   ```powershell
   python -m uvicorn main:app --reload
   ```
11. Visit http://127.0.0.1:8000. API documentation: http://127.0.0.1:8000/docs. Stop the server with Ctrl+C.
12. Run tests with `python -m pytest -q` (tests do not call Gemini).

## Features / endpoints
- `GET /` web interface
- `GET /health` status check
- `POST /qa` JSON `{"question":"What is the largest ocean?"}`
- `POST /explain` JSON `{"topic":"Photosynthesis","level":"Beginner"}`
- `POST /quiz` JSON `{"text":"Study passage..."}`
- `POST /summarize` JSON `{"text":"Passage to summarize..."}`
- `POST /learn/recommendations` JSON `{"topic":"SQL","level":"Beginner"}`

The quiz returns exactly three questions with four options each. AI output may be incorrect; verify important facts. API model names and availability can change; if Gemini reports an unavailable model, change `GEMINI_MODEL` in `.env` to a model available to your account.

## Optional local LaMini explanation model
This is optional and may download large model files on first use. Run `python -m pip install -r requirements-local-explanation.txt`, set `ENABLE_LOCAL_EXPLAINER=true` in `.env`, and restart. If the local model fails to load, the app falls back to Gemini.

## Troubleshooting
- `python` not recognized: install Python 3.10+ from https://www.python.org/downloads/ and tick Add Python to PATH; reopen VS Code.
- Module missing: activate `.venv` and reinstall requirements.
- API key missing: ensure `.env` is next to `main.py` and contains `GEMINI_API_KEY=...`.
- API auth/model error: verify the key and configured model.
- Port busy: run `python -m uvicorn main:app --reload --port 8001` and open http://127.0.0.1:8001.
- PowerShell activation issue: use Command Prompt activation or run `.venv\Scripts\python.exe -m pip install -r requirements.txt` without activating.

Security: local learning project only. Do not expose the development server publicly or share `.env`/API key.
