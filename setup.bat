@echo off
echo.
echo =========================================
echo    FactoryLink Setup Script
echo =========================================
echo.

REM Install uv if not already installed
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing uv (Python package manager)...
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo uv installed successfully.
    REM Refresh PATH
    set PATH=%USERPROFILE%\.cargo\bin;%LOCALAPPDATA%\uv\bin;%PATH%
) else (
    echo uv already installed.
)

echo.

REM Create .env file
echo Creating .env file...
(
echo DATABASE_URL=postgresql://neondb_owner:npg_ARlY7QfNJu3I@ep-fancy-feather-agfppv25-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require^&channel_binding=require
echo SECRET_KEY=LbfSwTI7LleizG0Q6hkZcC6RpUOeby0h3CaANQ22edS
echo ALGORITHM=HS256
echo ACCESS_TOKEN_EXPIRE_MINUTES=60
) > .env

REM Install Python 3.12 and all dependencies automatically
echo Installing Python 3.12 and dependencies...
echo (This may take a minute on first run)
uv sync

echo.
echo =========================================
echo    Setup complete!
echo =========================================
echo.
echo    Admin login:
echo    Email:    admin@factorylink.com
echo    Password: admin123
echo.
set /p answer="   Start the server now? (y/n): "
if /i "%answer%"=="y" (
    echo.
    echo Starting server...
    echo Open your browser at: http://localhost:8000
    echo Press CTRL+C to stop
    echo.
    uv run uvicorn main:app --reload
) else (
    echo.
    echo    To start later, run:
    echo    uv run uvicorn main:app --reload
    echo.
    echo    Then open: http://localhost:8000
    echo.
    pause
)
