@echo off
echo Setting up AgroMind AI Environment...
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo Setup complete! Run run.bat to start the application.
pause
