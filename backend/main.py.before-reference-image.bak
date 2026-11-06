
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.educator_loop.api import router as educator_router
from backend.llm_query import query_llm
from backend.avatar.router import router as avatar_router
from backend.database.router import router as database_router

from backend.lesson_generation.router import router as lesson_router

app = FastAPI(title="Adaptive Classroom API")

app.include_router(educator_router)
app.include_router(avatar_router)
app.include_router(database_router)
app.include_router(lesson_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/generate")
async def generate(request: PromptRequest):
    try:
        result = await query_llm(request.prompt)
        return {"response": result}
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="LLM generation failed"
        )
    