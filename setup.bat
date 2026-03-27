@echo off
echo.
echo =========================================
echo    FactoryLink Setup Script
echo =========================================
echo.

REM Check Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed.
    echo Please install it from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Found Python:
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv myvenv

REM Activate it
echo Activating virtual environment...
call myvenv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q

REM Create .env file
echo Creating .env file...
(
echo DATABASE_URL=postgresql://neondb_owner:npg_P6ChIG5KzTjd@ep-fancy-feather-agfppv25-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
echo SECRET_KEY=LbfSwTI7LleizG0Q6hkZcC6RpUOeby0h3CaANQ22edS
echo ALGORITHM=HS256
echo ACCESS_TOKEN_EXPIRE_MINUTES=60
) > .env

echo.
echo =========================================
echo    Setup complete!
echo =========================================
echo.
echo    Admin login:
echo    Email:    admin@factorylink.com
echo    Password: admin123
echo.
set /p answer=   Start the server now? (y/n): 
if /i "%answer%"=="y" (
    echo.
    echo Starting server...
    echo Open your browser at: http://localhost:8000
    echo Press CTRL+C to stop
    echo.
    uvicorn main:app --reload
) else (
    echo.
    echo    To start later, run:
    echo    myvenv\Scripts\activate
    echo    uvicorn main:app --reload
    echo.
    echo    Then open: http://localhost:8000
    echo.
)
pause
