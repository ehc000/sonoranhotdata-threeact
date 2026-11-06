from pathlib import Path
import re, shutil
root=Path(__file__).resolve().parents[2]
paths=[root/'frontend/src/components/lesson/LessonRenderer.tsx',root/'frontend/src/pages/teacher/Assignments.tsx']
changed=[]
for path in paths:
 if not path.exists():continue
 s=path.read_text(); t=s
 # Remove the previously introduced manual reference upload widget and its import.
 t=re.sub(r'^import\s+TeacherGeneratedScene\s+from\s+[\'\"]\./TeacherGeneratedScene[\'\"];?\s*\n','',t,flags=re.M)
 t=re.sub(r'^\s*<TeacherGeneratedScene\b[^>]*\/>(?:\s*\n)?','\n',t,flags=re.M)
 # If a legacy reference-artwork input is present as a self-contained JSX label, remove only that input.
 t=re.sub(r'<label\b[^>]*>\s*Reference (?:artwork|image)\s*<input\b[^>]*type=[\'\"]file[\'\"][^>]*/>\s*</label>','',t,flags=re.I)
 if t!=s:
  backup=path.with_suffix(path.suffix+'.before-hide-reference.bak');shutil.copy2(path,backup)
  path.write_text(t);changed.append(str(path.relative_to(root)))
print('Updated:', ', '.join(changed) if changed else 'No old manual reference-artwork widget found.')
print('The automatic AutoLessonArtwork component and backend style reference were preserved.')
