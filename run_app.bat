@echo off
echo Starting PromptPerfect Flask Application...
echo.

REM Set environment variables
set SESSION_SECRET=dev-secret-key-change-in-production
set GEMINI_API_KEY=placeholder-api-key-add-your-real-key-here

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found. Creating one...
    python -m venv .venv
    echo Installing requirements...
    ".venv\Scripts\pip.exe" install -r requirements.txt
)

REM Activate virtual environment and run the app
echo Activating virtual environment...
call ".venv\Scripts\activate.bat"

echo Starting Flask server...
echo The app will be available at http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
echo Note: To use Gemini API features, set your GEMINI_API_KEY in this file
echo.

".venv\Scripts\python.exe" app.py

pause
