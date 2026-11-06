#!/usr/bin/env python3
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
main=root/'backend/main.py'
render=root/'frontend/src/components/lesson/LessonRenderer.tsx'
assign=root/'frontend/src/pages/teacher/Assignments.tsx'
for f in (main,render,assign):
    if not f.exists(): raise SystemExit(f"Missing {f}; no files changed")
m=main.read_text(); r=render.read_text(); a=assign.read_text()
if 'AUTO_LESSON_ART_V1' in r:
    print("Automatic lesson artwork already installed");raise SystemExit(0)
anchor='<p className="eyebrow">MISSION LESSON · DEMO RENDERING</p>'
if anchor not in r: raise SystemExit("LessonRenderer version differs; no files changed")
if 'app = FastAPI(' not in m: raise SystemExit("FastAPI app declaration not found; no files changed")
# All changes additive; avoid touching question text or other UI
for f in (main,render):shutil.copy2(f,f.with_suffix(f.suffix+'.before-auto-art.bak'))
if 'from __future__ import annotations' in m:
    m=m.replace('from __future__ import annotations','from __future__ import annotations\nfrom backend import auto_scene_images',1)
else:
    # Import immediately before app declaration, not before potential module docstring
    idx=m.index('app = FastAPI(')
    m=m[:idx]+'from backend import auto_scene_images\n'+m[idx:]
m+='\n# AUTO_LESSON_ART_V1\napp.include_router(auto_scene_images.router)\n'
r="import AutoLessonArtwork from './AutoLessonArtwork';\n"+r
r=r.replace(anchor,anchor+'\n      {/* AUTO_LESSON_ART_V1: automatic image after assembly */}\n      <AutoLessonArtwork lesson={lesson} studentName={studentName} studentInterests={studentInterests} studentId={studentId} />',1)
# Extend renderer props if the existing teacher demo hasn't already done so
if 'studentId?: string' not in r:
    r=r.replace('type Props = { lesson: RenderableLesson;', 'type Props = { lesson: RenderableLesson; studentId?: string;',1)
    r=r.replace('export default function LessonRenderer({ lesson,', 'export default function LessonRenderer({ lesson, studentId,',1)
    if 'export default function LessonRenderer({ lesson }:' in r:
        r=r.replace('export default function LessonRenderer({ lesson }:', 'export default function LessonRenderer({ lesson, studentId }:',1)
if 'studentName' not in r.split('type Props =',1)[-1].split(';',1)[0]:
    # This is expected to be installed after Teacher_Student_Lesson_Pipeline_Demo
    pass
# Feed studentId through existing teacher call only if it is already present
if '<LessonRenderer ' in a and 'studentId={studentId}' not in a:
    import re
    a2=re.sub(r'(<LessonRenderer\b[^>]*?)(\s*/>)',r'\1 studentId={studentId}\2',a,count=1)
    if a2!=a:
        shutil.copy2(assign,assign.with_suffix(assign.suffix+'.before-auto-art.bak'))
        assign.write_text(a2)
main.write_text(m);render.write_text(r)
print("Automatic lesson image generation connected. Backup files created.")
