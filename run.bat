@echo off
echo Starting AgroMind AI...
set PYTHONPATH=%cd%
call venv\Scripts\activate.bat
streamlit run app/main.py
pause
