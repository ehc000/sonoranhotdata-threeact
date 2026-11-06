import { useEffect, useState } from 'react';

/** Automatic scene generation after assembly. Avatar remains a separate overlay.
 * No manual image upload, Generate button, or background regeneration on answer clicks.
 */
type Props = { lesson: unknown; studentId?: string; studentName?: string; studentInterests?: string };
const API = 'http://localhost:8000'; // shared VITE_API_URL restoration remains a separate TODO
export default function AutoLessonArtwork({ lesson, studentId, studentName, studentInterests }: Props) {
  const [url, setUrl] = useState<string | null>(null);
  const [status, setStatus] = useState<'loading'|'ready'|'error'>('loading');
  const [error, setError] = useState('');
  const [approved, setApproved] = useState(false);
  const [progress, setProgress] = useState(0);
  const [reduceMotion, setReduceMotion] = useState(false);
  const lessonKey = JSON.stringify(lesson);
  useEffect(() => {
    const controller = new AbortController();
    let localUrl: string | null = null;
    setStatus('loading');setError('');setApproved(false);setProgress(0);setUrl(null);
    (async () => {
      try {
        const r = await fetch(`${API}/api/lesson-art/generate`, {
          method:'POST', headers:{'Content-Type':'application/json'},
          body:JSON.stringify({lesson,student_interests:studentInterests || ''}),
          signal:controller.signal
        });
        if (!r.ok) {
          const data = await r.json().catch(()=>({}));
          throw new Error(typeof data.detail === 'string' ? data.detail : `HTTP ${r.status}`);
        }
        const blob = await r.blob();
        if (controller.signal.aborted) return;
        localUrl=URL.createObjectURL(blob);setUrl(localUrl);setStatus('ready');
      } catch(e) {
        if(!controller.signal.aborted){setError(e instanceof Error?e.message:String(e));setStatus('error')}
      }
    })();
    return ()=>{controller.abort();if(localUrl)URL.revokeObjectURL(localUrl)};
  // Only start a generation when lesson content or student interests change.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[lessonKey,studentInterests]);
  return <section aria-label="Automatic AI lesson illustration" style={{margin:'16px 0'}}>
    <h3 style={{margin:'0 0 8px'}}>Lesson artwork</h3>
    {status==='loading' && <p role="status">Generating the scene automatically from the lesson and saved reference style…</p>}
    {status==='error' && <p role="status" style={{color:'#a33'}}>AI image unavailable: {error}. The illustrated template below is still available.</p>}
    {url && <div>
      <div style={{position:'relative',aspectRatio:'3 / 2',overflow:'hidden',borderRadius:12,background:'#dcebf3'}}>
        <img src={url} alt="Generated background based on lesson storyline and reference style" style={{width:'100%',height:'100%',objectFit:'cover'}} />
        {approved && studentId && <img
          src={`${API}/avatar/${encodeURIComponent(studentId)}/render.svg`}
          alt={`${studentName||'Student'} avatar`}
          onError={e=>{e.currentTarget.style.display='none'}}
          style={{position:'absolute',left:`${10+progress*12}%`,bottom:'12%',width:'25%',height:'30%',objectFit:'cover',objectPosition:'left',clipPath:'inset(0 50% 0 0)',transform:'scale(1.5)',transformOrigin:'bottom left',transition:reduceMotion?'none':'left 400ms ease'}}
        />}
      </div>
      {!approved ? <div style={{marginTop:10}}>
        <p>Generated automatically. Review the scene before showing it to students.</p>
        <button type="button" onClick={()=>setApproved(true)}>Approve artwork for preview</button>
      </div> : <div style={{marginTop:10}}>
        <p style={{fontSize:13}}>Artwork approved · Avatar is a separate layer</p>
        {studentId ? <>
          <button type="button" onClick={()=>setProgress(p=>Math.min(5,p+1))} disabled={progress===5}>Advance avatar (demo)</button>
          <button type="button" onClick={()=>setProgress(0)} style={{marginLeft:8}}>Reset</button>
        </> : <p style={{fontSize:13}}>Select a student with a saved backend avatar to display the character. Mock student IDs are not automatically mapped.</p>}
        <label style={{display:'inline-flex',gap:6,alignItems:'center',marginLeft:12,padding:8,borderRadius:8,background:'#eef3f7'}}>
          <input type="checkbox" checked={reduceMotion} onChange={e=>setReduceMotion(e.target.checked)} /> Reduce motion
        </label>
      </div>}
    </div>}
  </section>;
}
