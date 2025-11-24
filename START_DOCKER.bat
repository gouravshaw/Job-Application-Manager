@echo off
echo ====================================
echo Job Application Manager - Docker
echo ====================================
echo.
echo Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo Docker is running!
echo.
echo Building and starting containers...
echo This may take a few minutes on first run...
echo.

docker-compose up --build

echo.
echo Application stopped.
pause

