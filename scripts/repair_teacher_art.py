#!/usr/bin/env python3
"""Idempotent, conservative patch of teacher lesson renderer and backend routes."""
from pathlib import Path
import re
import shutil

root = Path(__file__).resolve().parents[1]
src = root / 'frontend/src'
renderer = src / 'components/lesson/LessonRenderer.tsx'
main = root / 'backend/main.py'
if not renderer.is_file() or not main.is_file():
    raise SystemExit('Missing LessonRenderer.tsx or backend/main.py; nothing changed.')
original_r, original_m = renderer.read_text(), main.read_text()
r, m = original_r, original_m
# Remove the obsolete upload component from every consumer, not the source file itself.
changes = {}
for file in src.rglob('*.tsx'):
    if file.name == 'TeacherGeneratedScene.tsx':
        continue
    before = file.read_text()
    after = re.sub(r'^\s*import\s+TeacherGeneratedScene\s+from\s+[\'\"][^\'\"]+[\'\"];?\s*\n', '', before, flags=re.M)
    after = re.sub(r'^[ \t]*<TeacherGeneratedScene\b[\s\S]*?/\s*>[ \t]*\n?', '', after, flags=re.M)
    if after != before:
        changes[file] = after
        if file == renderer:
            r = after
# Remove any previously injected AutoLessonArtwork import/call, then inject exactly one.
r = re.sub(r'^\s*import\s+AutoLessonArtwork\s+from\s+[\'\"][^\'\"]+[\'\"];?\s*\n', '', r, flags=re.M)
r = re.sub(r'^[ \t]*\{\/\* AUTO_LESSON_ART_V1[^\n]*\n', '', r, flags=re.M)
r = re.sub(r'^[ \t]*<AutoLessonArtwork\b[\s\S]*?/\s*>[ \t]*\n?', '', r, flags=re.M)
anchor = '<p className="eyebrow">MISSION LESSON · DEMO RENDERING</p>'
if anchor not in r:
    raise SystemExit('Renderer structure differs; no changes made. Send LessonRenderer.tsx.')
# Only pass the guaranteed lesson prop. Student identity must be explicitly wired later.
r = "import AutoLessonArtwork from './AutoLessonArtwork';\n" + r
r = r.replace(anchor, anchor + '\n      <AutoLessonArtwork lesson={lesson} />', 1)
if 'app.include_router(auto_scene_images.router)' not in m:
    if 'from __future__ import annotations' in m:
        m = m.replace('from __future__ import annotations', 'from __future__ import annotations\nfrom backend import auto_scene_images', 1)
    else:
        idx = m.find('app = FastAPI(')
        if idx < 0:
            raise SystemExit('FastAPI app declaration not found; no changes made.')
        m = m[:idx] + 'from backend import auto_scene_images\n' + m[idx:]
    m += '\napp.include_router(auto_scene_images.router)\n'
elif 'from backend import auto_scene_images' not in m:
    idx = m.find('app = FastAPI(')
    if idx < 0:
        raise SystemExit('FastAPI app declaration not found; no changes made.')
    m = m[:idx] + 'from backend import auto_scene_images\n' + m[idx:]
# Commit only after all checks.
changes[renderer] = r
changes[main] = m
for file, after in changes.items():
    before = file.read_text()
    if before == after:
        continue
    shutil.copy2(file, file.with_suffix(file.suffix + '.before-auto-image-repair.bak'))
    file.write_text(after)
    print('Updated', file.relative_to(root))
print('Done. The old reference upload is removed; automatic image generation remains.')
