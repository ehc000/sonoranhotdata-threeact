"""Before/after illustrated story scenes. Mount router in existing FastAPI app."""
import base64
import hashlib
import json
import os
from collections import OrderedDict
from pathlib import Path

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/lesson-scene-pairs", tags=["lesson-scenes"])
STYLE = Path(__file__).parent / "assets" / "lesson_style_reference.png"
CACHE: OrderedDict[str, bytes] = OrderedDict()

class ScenePairRequest(BaseModel):
    lesson_id: str = Field(max_length=200)
    story_title: str = Field(max_length=300)
    setting: str = Field(max_length=1500)
    scene_number: int = Field(ge=0, le=60)
    total_scenes: int = Field(ge=1, le=62)
    scene_description: str = Field(max_length=2500)
    previous_scene_description: str = Field(default="", max_length=2000)
    phase: str = Field(pattern="^(before|after)$")

def signature(r: ScenePairRequest, phase: str) -> str:
    obj = r.model_dump() if hasattr(r, "model_dump") else r.dict()
    obj["phase"] = phase
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()

@router.post("/generate")
async def generate(req: ScenePairRequest):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise HTTPException(503, "OPENAI_API_KEY not configured")
    model = os.getenv("SCENE_IMAGE_MODEL", "gpt-image-1")
    sig = signature(req, req.phase) + ":" + model
    if sig in CACHE:
        CACHE.move_to_end(sig)
        return Response(CACHE[sig], media_type="image/png")
    # After frame is edited from the *actual before image* whenever it exists.
    before_key = signature(req, "before") + ":" + model
    prior = CACHE.get(before_key) if req.phase == "after" else None
    if prior is None and not STYLE.exists():
        raise HTTPException(503, "Missing backend/assets/lesson_style_reference.png")
    reference = prior if prior is not None else STYLE.read_bytes()
    prompt = f"""Create ONE frame of an original, coherent 16-bit pixel-art educational storybook.
This image is a continuation/edit of the supplied visual reference, not a new art direction.
HARD CONTINUITY CONSTRAINTS: preserve the EXACT same protagonist identity and recognizable appearance (hair, face, outfit, silhouette, colors, accessories, body proportions, pixel density). Preserve the exact same camera, side-view framing, scale, perspective, architecture, recognizable landmarks, background geometry, light direction, palette, outline thickness, and object locations. Never add extra characters or duplicates. No labels, text, numbers, equations, watermarks or UI.
If the reference is a style sheet rather than a story scene, use it as the canonical art style; draw one consistent student protagonist. If the reference is a scene, treat it as the canonical prior state and change only what the narrative requires.
TITLE: {req.story_title}
SETTING: {req.setting}
SCENE: {req.scene_number + 1}/{req.total_scenes}
PREVIOUS CONTEXT: {req.previous_scene_description}
CURRENT STORY ACTION: {req.scene_description}
STATE: {req.phase.upper()}
{"BEFORE: depict the protagonist about to perform the described action. Make the objective visually clear." if req.phase == "before" else "AFTER: same shot and exact same character, action now completed; show the consequence and changed objects. Preserve all unrelated pixels/composition as closely as possible."}
Use crisp pixel art, a landscape 3:2 composition, no writing in image."""
    try:
        async with httpx.AsyncClient(timeout=180) as client:
            response = await client.post(
                "https://api.openai.com/v1/images/edits",
                headers={"Authorization": f"Bearer {key}"},
                data={"model": model, "prompt": prompt, "size": "1536x1024"},
                files={"image": ("reference.png", reference, "image/png")},
            )
        if response.status_code >= 400:
            raise HTTPException(502, f"Image API HTTP {response.status_code}: {response.text[:450]}")
        png = base64.b64decode(response.json()["data"][0]["b64_json"])
    except HTTPException:
        raise
    except (ValueError, KeyError, IndexError, httpx.HTTPError) as exc:
        raise HTTPException(502, "Scene generation failed") from exc
    CACHE[sig] = png
    while len(CACHE) > 40:
        CACHE.popitem(last=False)
    return Response(png, media_type="image/png")
