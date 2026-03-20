@echo off
REM ============================================================
REM App Design Server (03_app_design) - Production
REM Port: 8102
REM Environment: production
REM ============================================================

echo Starting App Design Server (Port 8102)...

REM Set environment variable
set APP_ENVIRONMENT=production

REM Navigate to application directory and run server
pushd 03_app_design
uv run python manage.py runserver 0.0.0.0:8102
popd
pause
