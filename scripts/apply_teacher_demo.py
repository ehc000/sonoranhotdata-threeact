#!/usr/bin/env python3
# Apply additive teacher/student preview changes; back up existing files first.
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
a=root/'frontend/src/pages/teacher/Assignments.tsx'
b=root/'frontend/src/components/lesson/LessonRenderer.tsx'
for f in (a,b):
    if not f.exists(): raise SystemExit(f'Missing {f}; nothing changed')
s=a.read_text(); t=b.read_text()
if 'TEACHER_STUDENT_PIPELINE_DEMO_2026' in s:
    print('Already installed'); raise SystemExit(0)
anchors=['  const [studentId, setStudentId] = useState(', '      {assembledLesson && (', '<LessonRenderer key={assembledLesson.lesson_id} lesson={toRenderableLesson(assembledLesson)} />']
if not all(x in s for x in anchors) or 'type Props = { lesson: RenderableLesson };' not in t:
    raise SystemExit('Unexpected local file version. No files changed; please share current Assignments.tsx and LessonRenderer.tsx.')
# Snapshot before touching anything
for f in (a,b): shutil.copy2(f, f.with_suffix(f.suffix+'.before-teacher-demo.bak'))
# Student profile: use actual supplied student data; no invented fields or extra API assumptions.
s=s.replace('  const [objective, setObjective] = useState(\'\');', '''  // TEACHER_STUDENT_PIPELINE_DEMO_2026: The same selected student drives profile and lesson.
  const selectedStudent = students.find(item => item.id === studentId);
  const profile = selectedStudent as unknown as Record<string, unknown> | undefined;
  const profileText = (key: string) => {
    const v = profile?.[key];
    if (Array.isArray(v)) return v.filter(x => typeof x === 'string').join(', ');
    return typeof v === 'string' ? v : '';
  };
  const [objective, setObjective] = useState('');''',1)
anchor='        {/* ------------------------------------------------------------\n            AI-ASSISTED MODIFICATION: Competency before story generation.'
card='''        {/* TEACHER_STUDENT_PIPELINE_DEMO_2026: Teacher sees the real selected record. */}
        {selectedStudent && (
          <section aria-label="Selected student profile" style={{border:'1px solid #cbd5e1', borderRadius:12, padding:16, margin:'14px 0 20px', background:'#f8fafc'}}>
            <p className="eyebrow">SELECTED STUDENT PROFILE · TEACHER VIEW</p>
            <h3 style={{margin:'4px 0 8px'}}>{selectedStudent.name}</h3>
            {profileText('grade_level') && <p><strong>Grade:</strong> {profileText('grade_level')}</p>}
            {profileText('interests') && <p><strong>Interests:</strong> {profileText('interests')}</p>}
            {profileText('interests_text') && <p><strong>Interest notes:</strong> {profileText('interests_text')}</p>}
            {profileText('learning_preferences') && <p><strong>Learning preferences:</strong> {profileText('learning_preferences')}</p>}
            {profileText('learning_preferences_text') && <p><strong>Learning preferences:</strong> {profileText('learning_preferences_text')}</p>}
            {profileText('strengths') && <p><strong>Strengths:</strong> {profileText('strengths')}</p>}
            {profileText('supports') && <p><strong>Supports:</strong> {profileText('supports')}</p>}
            <p className="muted small">This shows fields available in the teacher student list. Missing details are not invented. Existing teacher notes remain unchanged.</p>
          </section>
        )}

'''
s=s.replace(anchor,card+anchor,1)
s=s.replace('<LessonRenderer key={assembledLesson.lesson_id} lesson={toRenderableLesson(assembledLesson)} />','''<LessonRenderer key={`${assembledLesson.lesson_id}:${studentId}`} lesson={toRenderableLesson(assembledLesson)} studentName={selectedStudent?.name} studentInterests={profileText('interests')} />''',1)
s=s.replace('          <h2>Student-facing lesson rendering</h2>','''          <h2>Student-facing lesson rendering</h2>
          <p><strong>Previewing as:</strong> {selectedStudent?.name ?? 'Selected student'}</p>''',1)
# Avoid accidentally presenting old lesson for newly selected student; already cleared on student change.
t=t.replace('type Props = { lesson: RenderableLesson };','type Props = { lesson: RenderableLesson; studentName?: string; studentInterests?: string };')
t=t.replace('export default function LessonRenderer({ lesson }: Props) {','export default function LessonRenderer({ lesson, studentName, studentInterests }: Props) {')
t=t.replace('      <p className="eyebrow">MISSION LESSON · DEMO RENDERING</p>','''      <p className="eyebrow">MISSION LESSON · DEMO RENDERING</p>
      {studentName && <div aria-label="Student preview context" style={{padding:'10px 14px',border:'1px solid #cbd5e1',borderRadius:10,marginBottom:12}}>
        <strong>Student view: {studentName}</strong>
        {studentInterests && <p className="muted small" style={{margin:'4px 0 0'}}>Interests: {studentInterests}</p>}
      </div>}''',1)
a.write_text(s); b.write_text(t)
print('Updated teacher profile panel and student-facing preview; backups created.')
