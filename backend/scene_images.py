"""Optional image-edit endpoint for teacher-approved reference-guided scene generation.
Requires OPENAI_API_KEY and httpx. Never puts API keys in browser code.
No images or reference files are persisted by this endpoint.
"""
import base64
import os
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
import httpx

router = APIRouter(prefix="/api/scene-images", tags=["scene-images"])
MAX_BYTES = 8 * 1024 * 1024
ALLOWED = {"image/png": "reference.png", "image/jpeg": "reference.jpg", "image/webp": "reference.webp"}

@router.post("/generate")
async def generate_scene(reference: UploadFile = File(...), prompt: str = Form(...)):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise HTTPException(503, "Image generation not configured: set OPENAI_API_KEY on the backend.")
    if reference.content_type not in ALLOWED:
        raise HTTPException(400, "Reference must be PNG, JPEG, or WebP.")
    data = await reference.read(MAX_BYTES + 1)
    if not data or len(data) > MAX_BYTES:
        raise HTTPException(400, "Reference image must be between 1 byte and 8 MB.")
    if len(prompt) > 8000:
        raise HTTPException(400, "Prompt is too long.")
    try:
        async with httpx.AsyncClient(timeout=150) as client:
            result = await client.post(
                "https://api.openai.com/v1/images/edits",
                headers={"Authorization": f"Bearer {key}"},
                data={"model": os.getenv("SCENE_IMAGE_MODEL", "gpt-image-1"), "prompt": prompt, "size": "1536x1024"},
                files={"image": (ALLOWED[reference.content_type], data, reference.content_type)},
            )
        if result.status_code >= 400:
            # Do not expose raw upstream errors containing private data.
            raise HTTPException(502, f"Image service returned HTTP {result.status_code}. Check backend configuration and account access.")
        payload = result.json()
        b64 = payload["data"][0]["b64_json"]
        return Response(content=base64.b64decode(b64), media_type="image/png", headers={"Cache-Control":"no-store"})
    except (httpx.HTTPError, ValueError, KeyError, IndexError) as exc:
        raise HTTPException(502, "Image service request failed; existing illustration fallback is still available.") from exc
