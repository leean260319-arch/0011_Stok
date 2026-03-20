#!/bin/bash
# ============================================================
# Streamlit Development Server (Server 01)
# Port: 8501
# Environment: development
# ============================================================

echo "Starting Streamlit Development Server (Port 8501)..."

# Set environment variable
export APP_ENVIRONMENT=development

# Navigate to application directory and run server
cd 02_1st_server && uv run streamlit run login.py
