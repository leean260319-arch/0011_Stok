@echo off
REM ============================================================
REM Streamlit Production Server (Server 01)
REM Port: 8101
REM Environment: production
REM ============================================================

echo Starting Streamlit Production Server (Port 8101)...
REM Set environment variable
set APP_ENVIRONMENT=production

REM Navigate to application directory and run server
pushd 02_1st_server
uv run streamlit run login.py --server.port 8101 --server.address 0.0.0.0
popd