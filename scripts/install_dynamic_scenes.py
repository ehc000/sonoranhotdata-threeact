from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
player=root/'frontend/src/components/lesson/TeacherLessonPlayer.tsx'
backend=root/'backend'
source=root/'backend/scene_sequence.py'
if not player.exists():raise SystemExit('Missing TeacherLessonPlayer.tsx. Install playable preview first.')
if not (backend/'main.py').exists():
    candidates=[p for p in backend.glob('*.py') if 'include_router' in p.read_text() and 'FastAPI' in p.read_text()]
    if len(candidates)!=1:raise SystemExit('Could not identify backend app entrypoint; no changes made. Please share backend app entrypoint.')
    main=candidates[0]
else:main=backend/'main.py'
s=player.read_text()
if 'useDynamicScene' in s:raise SystemExit('Already installed')
anchor="import LessonAvatarSprite from './LessonAvatarSprite';"
if anchor not in s:raise SystemExit('Player format unexpected; no changes made')
shutil.copy2(player,player.with_suffix('.tsx.before-dynamic-scenes.bak'))
s=s.replace(anchor,anchor+"\nimport { useDynamicScene } from './useDynamicScene';")
# Place AI image inside the existing SVG, behind the same saved avatar sprite.
s=s.replace('avatar:LessonAvatarChoice|null}', 'avatar:LessonAvatarChoice|null;imageUrl:string|null}')
s=s.replace('progress,finale,avatar}:', 'progress,finale,avatar,imageUrl}:')
s=s.replace("   {kind==='space'?", "   {!imageUrl&&(kind==='space'?", 1)
s=s.replace('fill="#719caa"/></>}', 'fill="#719caa"/></>)}')
s=s.replace('   <rect x="0" y="257"', '   {!imageUrl&&<rect x="0" y="257"')
s=s.replace('fill={earth}/>','fill={earth}/>}')
for kind in ['mine','space','forest','castle']:
    s=s.replace("{kind==='"+kind+"'?", "{!imageUrl&&kind==='"+kind+"'?")
s=s.replace('   <path d="M0 271H800"', '   {imageUrl&&<image href={imageUrl} x="0" y="0" width="800" height="360" preserveAspectRatio="xMidYMid slice"/>}\n   {!imageUrl&&<path d="M0 271H800"')
s=s.replace('strokeDasharray="30 10"/>','strokeDasharray="30 10"/>}')
s=s.replace(" const kind=sceneKind(lesson);", " const kind=sceneKind(lesson);\n const {imageUrl,status:artStatus}=useDynamicScene(lesson,phase,index);")
old="   <Background kind={kind} progress={questions.length?completed/questions.length:0} finale={phase==='finale'} avatar={avatar}/>"
new="""   <Background kind={kind} progress={questions.length?completed/questions.length:0} finale={phase==='finale'} avatar={avatar} imageUrl={imageUrl}/>
   <p style={{fontSize:12,color:'#64748b',marginTop:5}} aria-live="polite">{artStatus==='loading'?'Illustrating this story scene… showing template meanwhile':artStatus==='fallback'?'Illustration unavailable — showing interactive template':'AI-illustrated scene · animated avatar overlay'}</p>"""
if old not in s:raise SystemExit('Scene anchor missing; no changes made')
s=s.replace(old,new)
player.write_text(s)
ms=main.read_text()
if 'scene_sequence' not in ms:
    shutil.copy2(main,main.with_suffix('.py.before-dynamic-scenes.bak'))
    ms='from backend.scene_sequence import router as scene_sequence_router\n'.replace('\n','\n')+ms
    # avoid inserting before __future__ imports: move import after future imports
    if 'from __future__ import ' in ms:
        ms=ms.replace('from backend.scene_sequence import router as scene_sequence_router\n','')
        lines=ms.splitlines(keepends=True)
        i=max(j for j,l in enumerate(lines) if l.startswith('from __future__ import '))+1
        lines.insert(i,'from backend.scene_sequence import router as scene_sequence_router\n')
        ms=''.join(lines)
    # Include router after app instantiation at end of module; safe with normal FastAPI apps.
    ms+='\n# AI-assisted dynamic illustrated lesson frames\napp.include_router(scene_sequence_router)\n'
    main.write_text(ms)
print('Installed dynamic illustrated scene player and backend router:',main)
