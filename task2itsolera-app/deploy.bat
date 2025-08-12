@echo off
setlocal enabledelayedexpansion

REM Geological Analysis Application Deployment Script for Windows
REM This script automates the deployment process for the geological analysis application

echo 🚀 Starting Geological Analysis Application Deployment...
echo.

REM Check if Docker is installed
echo [INFO] Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo [SUCCESS] Docker and Docker Compose are available
echo.

REM Check if required files exist
echo [INFO] Checking required files...
set "missing_files="

if not exist "app.py" set "missing_files=!missing_files! app.py"
if not exist "requirements.txt" set "missing_files=!missing_files! requirements.txt"
if not exist "Dockerfile" set "missing_files=!missing_files! Dockerfile"
if not exist "docker-compose.yml" set "missing_files=!missing_files! docker-compose.yml"
if not exist "nginx.conf" set "missing_files=!missing_files! nginx.conf"

if not exist "task2itsolera" (
    echo [ERROR] Data directory 'task2itsolera' not found
    pause
    exit /b 1
)

if defined missing_files (
    echo [ERROR] Missing required files:!missing_files!
    pause
    exit /b 1
)

echo [SUCCESS] All required files are present
echo.

REM Stop existing containers
echo [INFO] Stopping existing containers...
docker-compose down --remove-orphans >nul 2>&1
echo [SUCCESS] Existing containers stopped
echo.

REM Build and start containers
echo [INFO] Building and starting containers...

echo [INFO] Building application image...
docker-compose build --no-cache
if errorlevel 1 (
    echo [ERROR] Failed to build application image
    pause
    exit /b 1
)

echo [INFO] Starting services...
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] Failed to start services
    pause
    exit /b 1
)

echo [SUCCESS] Containers started successfully
echo.

REM Wait for application to be ready
echo [INFO] Waiting for application to be ready...
set "attempt=1"
set "max_attempts=30"

:wait_loop
echo [INFO] Attempt !attempt!/!max_attempts! - Checking if application is ready...
curl -f http://localhost:5000/health >nul 2>&1
if not errorlevel 1 (
    echo [SUCCESS] Application is ready!
    goto :deployment_success
)

if !attempt! geq !max_attempts! (
    echo [ERROR] Application failed to start within expected time
    goto :deployment_failed
)

echo [INFO] Application not ready yet, waiting 10 seconds...
timeout /t 10 /nobreak >nul
set /a attempt+=1
goto :wait_loop

:deployment_success
echo.
echo [SUCCESS] Deployment completed successfully!
echo.
call :show_status
goto :end

:deployment_failed
echo.
echo [ERROR] Deployment failed!
echo.
echo [INFO] Checking container logs...
docker-compose logs
pause
exit /b 1

:show_status
echo [INFO] Deployment Status:
echo.
docker-compose ps
echo.
echo [INFO] Application URLs:
echo   - Main Application: http://localhost:5000
echo   - Through Nginx: http://localhost:80
echo   - Health Check: http://localhost:5000/health
echo.
echo [INFO] Useful Commands:
echo   - View logs: docker-compose logs -f
echo   - Stop services: docker-compose down
echo   - Restart services: docker-compose restart
echo   - Update and redeploy: deploy.bat
echo.
goto :eof

:end
echo.
echo Deployment script completed. Press any key to exit...
pause >nul
