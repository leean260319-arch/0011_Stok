@echo off
echo Starting debug capture... > capture_batch.log
uv run --with playwright python tmp/capture_debug.py >> capture_batch.log 2>&1
