"""Prepare persistent, sequential pixel-art backgrounds before lesson playback.
Student avatars are rendered separately by the frontend.
"""
import base64
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Literal

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

router = APIRouter(prefix='/api/lesson-sequences', tags=['lesson-sequences'])
ASSET_ROOT = Path(__file__).resolve().parent / 'generated_lesson_assets'
STYLE_REFERENCE = Path(__file__).resolve().parent / 'assets' / 'lesson_style_reference.png'

class SceneInstruction(BaseModel):
    description: str = Field(min_length=1, max_length=2500)
    action: str = Field(default='reveal', max_length=50)

class PrepareLessonRequest(BaseModel):
    lesson_id: str = Field(min_length=1, max_length=200)
    story_title: str = Field(max_length=300)
    setting: str = Field(max_length=1500)
    scenes: list[SceneInstruction] = Field(min_length=1, max_length=62)
    story_complexity: Literal['simple', 'moderate', 'rich'] = 'simple'

def safe_lesson_id(value: str) -> str:
    slug = re.sub(r'[^a-zA-Z0-9_-]', '_', value)[:50]
    digest = hashlib.sha256(value.encode()).hexdigest()[:12]
    return f'{slug}_{digest}'

def animation_for(action: str, complexity: str) -> dict:
    animations = {
        'mine': ('pickaxe_swing', 'ore_sparkles'),
        'collect': ('pickup', 'inventory_glow'),
        'build': ('place_blocks', 'construction_sparkles'),
        'walk': ('walk', 'none'),
        'open': ('open_chest', 'treasure_glow'),
    }
    motion, effect = animations.get(action, ('reveal', 'sparkles'))
    if complexity == 'simple':
        effect = 'none'
    return {'action': motion, 'effect': effect,
            'duration_ms': {'simple': 650, 'moderate': 1100, 'rich': 1500}[complexity]}

async def edit_scene(client: httpx.AsyncClient, reference: bytes, prompt: str,
                     api_key: str, model: str) -> bytes:
    response = await client.post(
        'https://api.openai.com/v1/images/edits',
        headers={'Authorization': f'Bearer {api_key}'},
        data={'model': model, 'prompt': prompt, 'size': '1536x1024'},
        files={'image': ('reference.png', reference, 'image/png')},
    )
    if response.status_code >= 400:
        raise HTTPException(502, f'Image generation failed (HTTP {response.status_code})')
    try:
        return base64.b64decode(response.json()['data'][0]['b64_json'], validate=True)
    except (ValueError, KeyError, IndexError) as exc:
        raise HTTPException(502, 'Unexpected image-generation response') from exc

@router.post('/prepare')
async def prepare_lesson(req: PrepareLessonRequest):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise HTTPException(503, 'OPENAI_API_KEY not configured')
    if not STYLE_REFERENCE.is_file():
        raise HTTPException(503, 'Lesson style reference is missing')
    model = os.getenv('SCENE_IMAGE_MODEL', 'gpt-image-1.5')
    lesson_dir = ASSET_ROOT / safe_lesson_id(req.lesson_id)
    lesson_dir.mkdir(parents=True, exist_ok=True)
    content = req.model_dump()
    content['model'] = model
    content['style_reference_sha256'] = hashlib.sha256(STYLE_REFERENCE.read_bytes()).hexdigest()
    fingerprint = hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
    # Fingerprinted subfolders prevent partial updates from replacing valid old scenes.
    version_dir = lesson_dir / fingerprint[:20]
    version_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = version_dir / 'manifest.json'
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
            if manifest.get('fingerprint') == fingerprint and all(
                (version_dir / f'scene_{i:03d}.png').is_file()
                for i in range(len(req.scenes))
            ):
                return manifest
        except (ValueError, OSError):
            pass
    density = {
        'simple': 'LOW: uncluttered, large readable shapes, very few props, minimal atmospheric detail',
        'moderate': 'MODERATE: balanced environment detail and a few consistent background props',
        'rich': 'RICH: detailed environment, layered scenery, atmospheric elements, but readable foreground',
    }[req.story_complexity]
    previous_image = STYLE_REFERENCE.read_bytes()
    prepared_scenes = []
    async with httpx.AsyncClient(timeout=180) as client:
        for index, scene in enumerate(req.scenes):
            prompt = f'''Create scene {index + 1} of {len(req.scenes)} in one continuous original pixel-art story.
Story: {req.story_title}
World: {req.setting}
Event: {scene.description}
This is a BEFORE or AFTER frame for a specific academic challenge when so labeled.
The BEFORE frame must clearly show the unsolved story obstacle; the AFTER frame
must show the visible result of the SAME obstacle being resolved. Keep camera,
landmarks and educational objects in the same positions across the pair.
Do not add mathematical labels or invented numeric quantities. Exact fractions,
counts, and geometry must be checked by the teacher; image generation alone
cannot guarantee mathematical correctness.
Character action for separate frontend sprite (DO NOT DRAW CHARACTER): {scene.action}
Visual density: {density}
The supplied image is a STYLE GUIDE for the first scene, and the previous completed
background for later scenes. Maintain its pixel density, palette, camera, landmarks,
architecture, spatial geography and completed environmental changes across frames.
Generate a SIDE-VIEW GAME BACKGROUND ONLY. NO characters, protagonists, people,
creatures, avatars, NPCs, or silhouettes. Leave a clear walkable foreground for a
separate student-created avatar sprite overlaid by the frontend.
Only change objects needed by this event. Never reset completed environmental actions.
No text, labels, equations, speech bubbles, or UI. Landscape pixel-art composition.'''
            try:
                image_bytes = await edit_scene(client, previous_image, prompt, api_key, model)
            except httpx.HTTPError as exc:
                raise HTTPException(502, f'Scene {index + 1} generation failed') from exc
            filename = f'scene_{index:03d}.png'
            (version_dir / filename).write_bytes(image_bytes)
            prepared_scenes.append({
                'index': index,
                'description': scene.description,
                'image_url': f'/api/lesson-sequences/assets/{safe_lesson_id(req.lesson_id)}/{fingerprint[:20]}/{filename}',
                'animation': animation_for(scene.action, req.story_complexity),
            })
            previous_image = image_bytes
    manifest = {'lesson_id': req.lesson_id, 'fingerprint': fingerprint, 'scenes': prepared_scenes}
    temporary = manifest_path.with_suffix('.tmp')
    temporary.write_text(json.dumps(manifest, indent=2))
    temporary.replace(manifest_path)
    return manifest

@router.get('/assets/{lesson_folder}/{version}/{filename}')
def get_versioned_lesson_asset(lesson_folder: str, version: str, filename: str):
    if not re.fullmatch(r'[A-Za-z0-9_-]+', lesson_folder) or not re.fullmatch(r'[a-f0-9]{20}', version):
        raise HTTPException(400, 'Invalid lesson path')
    if not re.fullmatch(r'scene_[0-9]{3}\.png', filename):
        raise HTTPException(400, 'Invalid image filename')
    path = ASSET_ROOT / lesson_folder / version / filename
    if not path.is_file():
        raise HTTPException(404, 'Scene image not found')
    return FileResponse(path, media_type='image/png')

# Keep old asset URLs working for previously generated previews.
@router.get('/assets/{lesson_folder}/{filename}')
def get_lesson_asset(lesson_folder: str, filename: str):
    if not re.fullmatch(r'[A-Za-z0-9_-]+', lesson_folder):
        raise HTTPException(400, 'Invalid lesson folder')
    if not re.fullmatch(r'scene_[0-9]{3}\.png', filename):
        raise HTTPException(400, 'Invalid image filename')
    path = ASSET_ROOT / lesson_folder / filename
    if not path.is_file():
        raise HTTPException(404, 'Scene image not found')
    return FileResponse(path, media_type='image/png')
