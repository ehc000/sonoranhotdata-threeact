# Starts the avatar screens on http://localhost:8501 (start the API first, in another terminal)
Set-Location $PSScriptRoot
.\.venv\Scripts\python.exe -m streamlit run ui/companion_app.py
