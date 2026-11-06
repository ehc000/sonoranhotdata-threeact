from pathlib import Path
import shutil
root = Path(__file__).resolve().parents[1]
player = root / 'frontend/src/components/lesson/TeacherLessonPlayer.tsx'
main = root / 'backend/main.py'
if not player.exists() or not main.exists():
    raise SystemExit('Expected TeacherLessonPlayer.tsx and backend/main.py. No changes made.')
s = player.read_text()
m = main.read_text()
if 'useScenePair' in s:
    print('Scene-pair integration already installed')
    raise SystemExit(0)
if "import LessonAvatarSprite from './LessonAvatarSprite';" not in s:
    raise SystemExit('Unexpected player version. No changes made.')
if 'const kind=sceneKind(lesson);' not in s:
    raise SystemExit('Unexpected scene player layout. No changes made.')
shutil.copy2(player, player.with_suffix('.tsx.before-scene-pairs.bak'))
shutil.copy2(main, main.with_suffix('.py.before-scene-pairs.bak'))
s = s.replace("import LessonAvatarSprite from './LessonAvatarSprite';", "import LessonAvatarSprite from './LessonAvatarSprite';\nimport { useScenePair } from './useScenePair';")
s = s.replace(' const kind=sceneKind(lesson);', ' const kind=sceneKind(lesson);\n const scenePair=useScenePair(lesson,phase,index);\n const showAfter=phase===\'success\'||phase===\'finale\';')
# Keep fallback scene, but hide sliding sprite when generated artwork is present.
s = s.replace('avatar:LessonAvatarChoice|null;imageUrl:string|null}', 'avatar:LessonAvatarChoice|null;imageUrl:string|null;hideAvatar?:boolean}')
s = s.replace('progress,finale,avatar,imageUrl}:', 'progress,finale,avatar,imageUrl,hideAvatar}:')
s = s.replace('avatar:LessonAvatarChoice|null}', 'avatar:LessonAvatarChoice|null;hideAvatar?:boolean}')
s = s.replace('progress,finale,avatar}:', 'progress,finale,avatar,hideAvatar}:')
s = s.replace('   <g style={{transform:', '   {!hideAvatar&&<g style={{transform:')
s = s.replace('     <LessonAvatarSprite choice={avatar}/>\n   </g>', '     <LessonAvatarSprite choice={avatar}/>\n   </g>}')
# Replace old scene rendering with pair overlay, with simple crossfade, zoom and sparkles.
start=s.find('   <Background kind={kind} progress=')
end=s.find('\n',start)
if start<0:raise SystemExit('Could not find background call. No changes made.')
old=s[start:end]
# Image scene displayed as separate img, preserving a fallback to existing SVG scene.
new="""   <div style={{position:'relative',width:'100%',overflow:'hidden',borderRadius:12}}>
     <Background kind={kind} progress={questions.length?completed/questions.length:0} finale={phase==='finale'} avatar={avatar} imageUrl={null} hideAvatar={Boolean(scenePair.before)}/>
     {scenePair.before&&<img alt="Illustrated scene before the challenge" src={scenePair.before} style={{position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'cover',opacity:showAfter&&scenePair.after?0:1,transition:'opacity 650ms ease',transform:showAfter?'scale(1.015)':'scale(1)',imageRendering:'pixelated'}}/>}
     {scenePair.after&&<img alt="Illustrated scene after completing the challenge" src={scenePair.after} style={{position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'cover',opacity:showAfter?1:0,transition:'opacity 650ms ease',transform:showAfter?'scale(1.025)':'scale(1)',imageRendering:'pixelated'}}/>}
     {showAfter&&scenePair.after&&<span aria-hidden="true" style={{position:'absolute',top:'12%',right:'18%',fontSize:30,animation:'scene-pair-pop 650ms ease'}}>✨</span>}
   </div>
   <style>{`@keyframes scene-pair-pop {from {opacity:0;transform:scale(.4) rotate(-15deg)} to {opacity:1;transform:scale(1) rotate(0)}} @media (prefers-reduced-motion: reduce) {img {transition:none!important;transform:none!important}}`}</style>
   <p style={{fontSize:12,color:'#64748b'}}>{scenePair.loading?'Preparing illustrated story frames…':scenePair.error?'Image unavailable; showing playable fallback':'Illustrated before/after scene'}</p>"""
if 'imageUrl:string|null' not in s:
    new=new.replace(' imageUrl={null}', '')
s=s[:start]+new+s[end:]
# Remove older hook usage to avoid duplicate image API calls, if present.
s=s.replace("import { useDynamicScene } from './useDynamicScene';\n", '')
s=s.replace(" const {imageUrl,status:artStatus}=useDynamicScene(lesson,phase,index);\n", '')
s=s.replace("   <p style={{fontSize:12,color:'#64748b',marginTop:5}} aria-live=\"polite\">{artStatus==='loading'?'Illustrating this story scene… showing template meanwhile':artStatus==='fallback'?'Illustration unavailable — showing interactive template':'AI-illustrated scene · animated avatar overlay'}</p>\n", '')
# Make no accidental undefined imageUrl variable remain.
player.write_text(s)
if 'lesson_scene_pairs' not in m:
    lines=m.splitlines(keepends=True)
    insertion='from backend.lesson_scene_pairs import router as lesson_scene_pairs_router\n'
    future=[i for i,l in enumerate(lines) if l.startswith('from __future__ import')]
    lines.insert(max(future)+1 if future else 0,insertion)
    m=''.join(lines)+"\napp.include_router(lesson_scene_pairs_router)\n"
    main.write_text(m)
print('Installed before/after scene transitions and router. Backups saved.')
