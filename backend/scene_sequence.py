"""AI scene illustrations with strict visual continuity; no avatar baked into scene."""
import base64
import hashlib
import json
import os
from pathlib import Path
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/lesson-scenes", tags=["lesson-scenes"])
STYLE = Path(__file__).parent / "assets" / "lesson_style_reference.png"
_CACHE: dict[str, bytes] = {}

class SceneRequest(BaseModel):
    lesson_id: str = Field(max_length=200)
    story_title: str = Field(max_length=300)
    setting: str = Field(max_length=1500)
    stage: str = Field(max_length=50)
    scene_number: int = Field(ge=0, le=50)
    total_scenes: int = Field(ge=1, le=60)
    scene_description: str = Field(max_length=2500)
    previous_scene_description: str = Field(default="", max_length=2000)

@router.post("/generate")
async def generate_scene(req: SceneRequest):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise HTTPException(503, "Image API key is not configured")
    if not STYLE.is_file():
        raise HTTPException(503, "Saved style reference is missing")
    model = os.getenv("SCENE_IMAGE_MODEL", "gpt-image-1")
    # Model availability varies by account/provider. A 400 must not silently be presented as success.
    payload = req.model_dump() if hasattr(req, "model_dump") else req.dict()
    signature = hashlib.sha256((json.dumps(payload, sort_keys=True) + model).encode()).hexdigest()
    if signature in _CACHE:
        return Response(_CACHE[signature], media_type="image/png")
    prompt = f"""Create exactly ONE original side-view 16-bit pixel-art GAME BACKGROUND for a continuous educational adventure.
The supplied image is the CANONICAL STYLE BIBLE, not a scene to copy literally. Match its pixel density, pixel edge crispness, outlines, texture granularity, shading technique, palette harmony, and overall visual language. Do not switch to painterly, 3D, anime, photorealistic, vector, or another pixel-art style.

ABSOLUTE CONTINUITY RULES:
- All frames belong to ONE world in ONE lesson, with one persistent camera and 2D side-view perspective. Keep the horizon height, tile size, sprite scale, ground baseline at about 74% of image height, consistent lighting direction and color grading.
- Maintain geography and architecture across consecutive scenes: recurring tunnels, buildings, paths, trees, rock formations, machinery, props, entrances, and landmarks must keep their colors, construction, and relative positions. Change only what the scene's narrative calls for.
- Do not reset the environment between frames, change time of day, teleport objects, or introduce unrelated scenery. Reuse recognizable landmarks for spatial continuity.
- This is the same student character throughout, but DO NOT draw that character: the frontend will overlay the exact saved avatar sprite. Never include a person, humanoid, miner, student, face, mascot, NPC, silhouette, duplicate avatar, or character shadow. Do not add a placeholder person.
- Reserve clear unobstructed walking space across the lower-middle area for the avatar overlay, with visible objects for the avatar to approach or interact with. Keep interactable objects separated from that walking space.
- Do not add text, numbers, equations, UI, speech bubbles, watermarks, or question answers to the image.
- Illustrate the exact approved activity, not a generic setting. Keep the same world even when the activity changes.

CANONICAL LESSON TITLE: {req.story_title}
WORLD SETTING: {req.setting}
FRAME: {req.scene_number + 1} of {req.total_scenes}; phase {req.stage}
PREVIOUS SCENE CONTEXT (continuity only): {req.previous_scene_description}
THIS SCENE'S APPROVED STORY ACTION AND OBJECTS: {req.scene_description}

Compose a beautiful, legible 3:2 landscape game background. The avatar is composited separately. No text."""
    try:
        async with httpx.AsyncClient(timeout=180) as client:
            r = await client.post(
                "https://api.openai.com/v1/images/edits",
                headers={"Authorization": f"Bearer {key}"},
                data={"model": model, "prompt": prompt, "size": "1536x1024"},
                files={"image": ("style-reference.png", STYLE.read_bytes(), "image/png")},
            )
        if r.status_code >= 400:
            detail = "Image service rejected model or request" if r.status_code == 400 else "Image service unavailable"
            raise HTTPException(502, f"{detail} (upstream HTTP {r.status_code}). Check SCENE_IMAGE_MODEL and account access.")
        png = base64.b64decode(r.json()["data"][0]["b64_json"])
    except HTTPException:
        raise
    except (httpx.HTTPError, ValueError, KeyError, IndexError) as exc:
        raise HTTPException(502, "Scene generation failed") from exc
    if len(_CACHE) >= 25:
        _CACHE.pop(next(iter(_CACHE)))
    _CACHE[signature] = png
    return Response(png, media_type="image/png", headers={"Cache-Control": "no-store"})
