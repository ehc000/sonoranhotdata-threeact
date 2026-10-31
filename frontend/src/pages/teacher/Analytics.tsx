import type { Student } from '../../types';
import ProgressBar from '../../components/ProgressBar';
export default function Analytics({students}:{students:Student[]}) {return <div className="page narrow"><p className="eyebrow">TEACHER INSIGHTS</p><h1>Learning analytics</h1><p className="lead">Illustrative progress metrics, not validated assessments.</p><div className="card"><h2>Concept mastery snapshot</h2>{students.map(s=><div className="analytics-item" key={s.id}><ProgressBar value={s.mastery} label={s.name}/></div>)}</div></div>}
