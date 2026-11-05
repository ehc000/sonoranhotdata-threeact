"""Starts only the avatar router, for local demos.

backend/main.py also loads the other modules, which may not start yet.
Run from the project root: python -m uvicorn tools.demo_api:app --port 8000
The demo database goes in .claude/, which Git ignores, so demo students never reach the repo.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEMO_DB = ROOT / ".claude" / "avatar_demo.db"
DEMO_DB.parent.mkdir(exist_ok=True)
os.environ.setdefault("AVATAR_DB_PATH", str(DEMO_DB))  # must be set before the router loads storage
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI  # noqa: E402

from backend.avatar.router import router  # noqa: E402

app = FastAPI(title="Avatar demo (local)")
app.include_router(router)
