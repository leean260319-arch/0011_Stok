@echo off
REM ============================================================
REM OCR 모델 비교 - Streamlit Development Server
REM Port: 8501
REM Environment: development
REM ============================================================

echo Starting OCR Comparison Streamlit Server (Port 8501)...

REM Set environment variable
set APP_ENVIRONMENT=development

REM Run Streamlit from current directory
uv run streamlit run app.py
