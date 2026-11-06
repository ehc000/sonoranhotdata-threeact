from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[2]
main=root/'backend/main.py'
renderer=root/'frontend/src/components/lesson/LessonRenderer.tsx'
for path in (main,renderer):
    if not path.exists():
        print(f'SKIP missing: {path}')
        continue
    content=path.read_text()
    if path==main:
        old=path.with_suffix(path.suffix+'.before-reference-image.bak')
        if old.exists():
            shutil.copy2(old,path)
            print('Restored backend/main.py from original backup')
        else:
            content=content.replace('from backend import scene_images\n','')
            content=content.replace('\n# AI-assisted reference-guided image endpoint\napp.include_router(scene_images.router)\n','\n')
            content=content.replace('app.include_router(scene_images.router)','')
            path.write_text(content)
            print('Removed image router registration from backend/main.py')
    else:
        old=path.with_suffix(path.suffix+'.before-reference-image.bak')
        if old.exists():
            shutil.copy2(old,path)
            print('Restored LessonRenderer.tsx from original backup')
        else:
            import re
            content=re.sub(r"^import TeacherGeneratedScene from ['\"]\./TeacherGeneratedScene['\"];\s*\n",'',content,flags=re.M)
            content=re.sub(r'^\s*<TeacherGeneratedScene\b[^\n]*/>\s*\n','\n',content,flags=re.M)
            path.write_text(content)
            print('Removed manual generation component from LessonRenderer.tsx')
print('Rollback complete. Existing teacher student-profile and illustrated preview integrations are preserved as far as backups allow.')
