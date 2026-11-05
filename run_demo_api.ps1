# Starts the avatar API on http://localhost:8000 (docs at /docs)
Set-Location $PSScriptRoot
.\.venv\Scripts\python.exe -m uvicorn tools.demo_api:app --port 8000
