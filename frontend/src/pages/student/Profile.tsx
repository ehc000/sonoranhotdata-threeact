/** AI-assisted integration (GPT-6, 2026-11-05): replace emoji with Miguel's avatar. */
import type { Student } from '../../types';
import ProgressBar from '../../components/ProgressBar';
import MiguelAvatar from '../../components/MiguelAvatar';
export default function Profile({student,onNavigate}:{student:Student;onNavigate:(page:string)=>void}) {
  return <div className="page narrow"><p className="eyebrow">ABOUT ME</p><h1>My learning profile</h1><div className="card profile-card"><div className="profile-avatar"><MiguelAvatar studentId={student.id}/></div><h2>{student.name}</h2><p className="muted">Your learning space, your way.</p><button className="btn ghost" onClick={()=>onNavigate('Avatar')}>Customize avatar</button><div className="detail-row"><span>Interests</span><strong>{student.interests.join(', ')||'None yet'}</strong></div><div className="detail-row"><span>Learning format</span><strong>{student.format}</strong></div><div className="detail-row"><span>Pacing</span><strong>{student.pace}</strong></div><div className="detail-row"><span>Lessons completed</span><strong>{student.completed}</strong></div><ProgressBar value={student.mastery} label="Example mastery"/><button className="btn primary" onClick={()=>onNavigate('Calibration')}>Edit preferences</button></div></div>;
}
