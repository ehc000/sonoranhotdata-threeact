"""Reference-guided teacher lesson image generation. Never bake in a student avatar."""
import base64
import hashlib
import json
import os
from pathlib import Path

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

router = APIRouter(prefix='/api/lesson-art', tags=['lesson-art'])
REFERENCE = Path(__file__).parent / 'assets' / 'lesson_style_reference.png'
CACHE = {}

class GenerateRequest(BaseModel):
    lesson: dict
    student_interests: str = ''

@router.post('/generate')
async def generate(request: GenerateRequest):
    key = os.getenv('OPENAI_API_KEY')
    if not key:
        raise HTTPException(503, 'OPENAI_API_KEY is not configured in the backend process')
    if not REFERENCE.is_file():
        raise HTTPException(503, 'Internal lesson style reference image is missing')
    lesson_json = json.dumps(request.lesson, ensure_ascii=False, default=str)
    if len(lesson_json) > 20000:
        raise HTTPException(413, 'Lesson payload exceeds 20,000 characters')
    signature = hashlib.sha256((lesson_json + request.student_interests).encode()).hexdigest()
    if signature in CACHE:
        return Response(CACHE[signature], media_type='image/png')
    prompt = (
        'Create an ORIGINAL pixel-art educational game BACKGROUND using the attached image only '
        'as a reference for visual style, pixel density, palette and side-view composition. '
        'Use the approved lesson story and scene prompts to choose an appropriate setting; '
        'do not copy the castle unless the story calls for it. Leave a clear path for a separately '
        'overlaid player sprite. Absolutely NO people, animals, characters, avatars, lettering, '
        'numbers, equations, logos, buttons, or UI. Lesson: ' + lesson_json[:9000] +
        '. Student interests (environment details only): ' + request.student_interests[:300]
    )
    try:
        async with httpx.AsyncClient(timeout=180) as client:
            response = await client.post(
                'https://api.openai.com/v1/images/edits',
                headers={'Authorization': f'Bearer {key}'},
                data={
                    'model': os.getenv('SCENE_IMAGE_MODEL', 'gpt-image-1'),
                    'prompt': prompt,
                    'size': '1536x1024',
                },
                files={'image': ('lesson-style.png', REFERENCE.read_bytes(), 'image/png')},
            )
    except httpx.HTTPError as exc:
        raise HTTPException(502, 'Image API connection failed') from exc
    if response.status_code >= 400:
        # Preserve actionable error type/message without exposing upstream request data or keys.
        try:
            err = response.json().get('error', {})
            kind = str(err.get('code') or err.get('type') or 'request_error')[:80]
            message = str(err.get('message') or 'Request rejected')[:450]
        except (ValueError, AttributeError):
            kind, message = 'request_error', 'Request rejected'
        raise HTTPException(502, f'Image API HTTP {response.status_code} ({kind}): {message}')
    try:
        result = response.json()
        png = base64.b64decode(result['data'][0]['b64_json'], validate=True)
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise HTTPException(502, 'Image API returned an unexpected response format') from exc
    if len(CACHE) >= 12:
        CACHE.pop(next(iter(CACHE)))
    CACHE[signature] = png
    return Response(png, media_type='image/png', headers={'Cache-Control': 'no-store'})
