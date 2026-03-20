@echo off
REM ============================================================
REM Streamlit Development Server (Server 01)
REM Port: 8501
REM Environment: development
REM ============================================================

echo Starting Streamlit Development Server (Port 8501)...

REM Set environment variable
set APP_ENVIRONMENT=development

REM Navigate to application directory and run server
pushd 02_1st_server
uv run streamlit run login.py
popd