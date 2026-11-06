from pathlib import Path
import re, shutil
root=Path(__file__).resolve().parents[1]
renderer=root/"frontend/src/components/lesson/LessonRenderer.tsx"
player=root/"frontend/src/components/lesson/TeacherLessonPlayer.tsx"
if not renderer.exists() or not player.exists():
    raise SystemExit("Expected lesson files missing. Run from repository root.")
s=renderer.read_text()
p=player.read_text()
shutil.copy2(renderer, renderer.with_suffix(".tsx.before-ts-fix.bak"))
shutil.copy2(player, player.with_suffix(".tsx.before-ts-fix.bak"))
# Original installer removed only the first declaration in a multiline Props type,
# leaving an orphaned line beginning studentId?:.
s=re.sub(r"(?m)^\s*studentId\?: string; studentName\?: string; studentInterests\?: string \};\s*$", "", s)
# Ensure imported component appears before default export, not in the middle of code.
s=s.replace("import TeacherLessonPlayer from './TeacherLessonPlayer';", "")
s="import TeacherLessonPlayer from './TeacherLessonPlayer';\n"+s
# Avoid unused destructured props in strict TypeScript.
s=s.replace("export default function LessonRenderer({lesson,studentName,studentInterests,studentId}:{", "export default function LessonRenderer({lesson,studentName,studentInterests,studentId}:{")
# Remove unused imported type.
p=p.replace("import type { RenderableLesson, LessonQuestion } from './LessonRenderer';", "import type { RenderableLesson } from './LessonRenderer';")
renderer.write_text(s)
player.write_text(p)
print("Patched orphaned Props declaration and unused import. Backups created.")
