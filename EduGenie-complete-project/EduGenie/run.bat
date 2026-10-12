@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3 -m venv .venv
  if errorlevel 1 python -m venv .venv
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if not exist ".env" (
  copy ".env.example" ".env" >nul
  echo Add your Gemini API key to .env, save it, then run run.bat again.
  notepad ".env"
  pause
  exit /b 0
)
python -m uvicorn main:app --reload
pause
