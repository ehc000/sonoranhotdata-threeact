#!/usr/bin/env python3
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
main=root/'backend/main.py'
renderer=root/'frontend/src/components/lesson/LessonRenderer.tsx'
if not main.exists() or not renderer.exists():
    raise SystemExit("Expected backend/main.py and frontend/src/components/lesson/LessonRenderer.tsx. Nothing changed.")
m=main.read_text(); s=renderer.read_text()
if "scene_images.router" in m or "TeacherGeneratedScene" in s:
    raise SystemExit("Already installed (or partially installed). Review files before retrying.")
anchor='<p className="eyebrow">MISSION LESSON · DEMO RENDERING</p>'
if anchor not in s:
    raise SystemExit("LessonRenderer has changed; expected mission eyebrow anchor not found. Nothing changed.")
if "app = FastAPI(" not in m:
    raise SystemExit("Could not find FastAPI app declaration. Nothing changed.")
for f in (main,renderer):
    shutil.copy2(f,f.with_suffix(f.suffix+'.before-reference-image.bak'))
m="from backend import scene_images\n"+m if not m.startswith('"""') else m
# avoid breaking a possible future import by placing import after __future__ if present
if 'from __future__ import annotations' in m:
    m=m.replace('from backend import scene_images\n','').replace('from __future__ import annotations','from __future__ import annotations\nfrom backend import scene_images',1)
m+="\n# AI-assisted reference-guided image endpoint\napp.include_router(scene_images.router)\n"
s="import TeacherGeneratedScene from './TeacherGeneratedScene';\n"+s
# lesson may be teacher-rendered without studentId; profile name from earlier patch available
student='studentName={studentName}' if 'studentName' in s else ''
s=s.replace(anchor,anchor+f'\n      <TeacherGeneratedScene lesson={{lesson}} {student} />',1)
main.write_text(m);renderer.write_text(s)
print("Installed image generation endpoint + teacher preview. Backups saved.")
