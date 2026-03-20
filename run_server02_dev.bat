@echo off
REM ============================================================
REM App Design Server (03_app_design)
REM Port: 8000
REM Environment: development
REM ============================================================

echo Starting App Design Server (Port 8000)...

REM Set environment variable
set APP_ENVIRONMENT=development

REM Navigate to application directory and run server
pushd 03_app_design
uv run python manage.py runserver 0.0.0.0:8000
popd
pause