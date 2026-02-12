@echo off
echo ========================================
echo    Advanced Cover Letter Generator
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

echo Python found!
echo.

REM Install dependencies
echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully!
echo.

REM Start the Flask server
echo Starting Advanced Cover Letter Generator Web Server...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python backend\api.py

pause
