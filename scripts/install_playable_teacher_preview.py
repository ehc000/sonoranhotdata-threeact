from pathlib import Path
import shutil,re
root=Path(__file__).resolve().parents[1]
file=root/'frontend/src/components/lesson/LessonRenderer.tsx'
if not file.exists():raise SystemExit('LessonRenderer.tsx missing')
s=file.read_text()
if "TeacherLessonPlayer" in s:
 print('Already installed');raise SystemExit(0)
if "export default function LessonRenderer(" not in s:
 raise SystemExit('Unrecognized LessonRenderer; no changes made')
# Preserve exported RenderableLesson types and existing renderer code. Replace only its default render entrypoint.
# Make sure old renderer remains available for rollback.
shutil.copy2(file,file.with_suffix('.tsx.before-playable-preview.bak'))
# Existing Props can carry additional student fields; this wrapper avoids dependence on exact prop definitions.
replacement="""
import TeacherLessonPlayer from './TeacherLessonPlayer';
export default function LessonRenderer({lesson,studentName,studentInterests,studentId}:{
 lesson:RenderableLesson;studentName?:string;studentInterests?:string;studentId?:string
}){
 return <TeacherLessonPlayer lesson={lesson} studentName={studentName} studentInterests={studentInterests} studentId={studentId}/>;
}
"""
# Keep exported types; remove old default component and any unused imports/types.
i=s.index('export default function LessonRenderer(')
types=s[:i]
types=re.sub(r"import \{ useEffect, useState \} from 'react';\s*", '',types)
types=re.sub(r"type Screen = .*?;\s*", '',types)
types=re.sub(r"type Props = .*?;\s*", '',types)
file.write_text(types+replacement)
print('Installed playable teacher preview. Original backed up at',file.with_suffix('.tsx.before-playable-preview.bak'))
