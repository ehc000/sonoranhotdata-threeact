/** Student profile demo: compact avatar preview and editable learning preferences. */
import type { Student } from '../../types';
import ProgressBar from '../../components/ProgressBar';
import LessonAvatarSprite from '../../components/lesson/LessonAvatarSprite';
import type { LessonAvatarChoice } from '../../components/lesson/LessonAvatarSprite';
const demoChoice: LessonAvatarChoice = {base:'animal',head:'animal_cat',eyes:'round',primary_color:'#A8C5DA'};
function getPreview(): LessonAvatarChoice { try { const raw=localStorage.getItem('sonoran-lesson-avatar-preview'); return raw ? JSON.parse(raw) as LessonAvatarChoice : demoChoice; } catch {return demoChoice;} }
export default function Profile({student,onNavigate}:{student:Student;onNavigate:(page:string)=>void}) {
  const choice=getPreview();
  return <div className="page narrow"><p className="eyebrow">ABOUT ME · DEMO PROFILE</p><h1>My learning profile</h1>
    <div className="card profile-card" style={{textAlign:'left',maxWidth:760,margin:'auto'}}>
      <div style={{display:'flex',alignItems:'center',gap:20,flexWrap:'wrap',marginBottom:18}}>
        <div style={{width:120,height:140,flex:'0 0 120px',borderRadius:16,background:'#edf3f8',display:'grid',placeItems:'center'}}>
          <svg viewBox="0 0 100 110" width="105" height="116" role="img" aria-label="Current pixel-art demo avatar"><g transform="translate(8 8)"><LessonAvatarSprite choice={choice}/></g></svg>
        </div>
        <div style={{flex:1,minWidth:180}}><h2 style={{margin:'0 0 5px'}}>{student.name}</h2><p className="muted">Your learning space, your way.</p><button className="btn ghost" onClick={()=>onNavigate('Avatar')}>Customize avatar →</button></div>
      </div>
      <p className="muted small">DEMO PROFILE · Fictional student information and sample progress. Avatar choices are browser-local.</p>
      <div className="detail-row"><span>Interests</span><strong>{student.interests.join(', ')||'None yet'}</strong></div>
      <div className="detail-row"><span>Learning format</span><strong>{student.format}</strong></div>
      <div className="detail-row"><span>Pacing</span><strong>{student.pace}</strong></div>
      <div className="detail-row"><span>Demo lessons completed</span><strong>{student.completed}</strong></div>
      <ProgressBar value={student.mastery} label="Example progress (mock)"/>
      <button className="btn primary" onClick={()=>onNavigate('Calibration')}>Edit learning preferences</button>
    </div>
  </div>;
}
