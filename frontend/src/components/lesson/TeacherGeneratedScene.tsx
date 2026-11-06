/// <reference types="vite/client" />
import { useEffect, useState } from 'react';

/** Teacher-controlled image generation with a reference image.
 * Generated background and student avatar are SEPARATE layers.
 * Images are never generated on every answer or avatar movement.
 */
type Props = { lesson: unknown; studentId?: string; studentName?: string };
const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export default function TeacherGeneratedScene({lesson,studentId,studentName}:Props) {
  const [reference,setReference]=useState<File|null>(null);
  const [background,setBackground]=useState<string|null>(null);
  const [approved,setApproved]=useState(false);
  const [busy,setBusy]=useState(false);
  const [error,setError]=useState('');
  const [position,setPosition]=useState(15);
  const [reduceMotion,setReduceMotion]=useState(false);
  useEffect(()=>()=>{if(background?.startsWith('blob:'))URL.revokeObjectURL(background)},[background]);
  const generate=async()=>{
    if(!reference)return;
    setBusy(true);setError('');setApproved(false);
    try{
      const form=new FormData();
      form.append('reference',reference);
      form.append('prompt',`Make a visually consistent, polished 2D educational game BACKGROUND inspired by the uploaded reference. Preserve its artistic style, color palette, and scene perspective. Based on this lesson: ${JSON.stringify(lesson).slice(0,3500)}. Include a clear path for a character to move across the scene. IMPORTANT: Do NOT draw any characters, people, mascots, text, numbers, equations, or interface elements. Background only.`);
      const r=await fetch(`${API}/api/scene-images/generate`,{method:'POST',body:form});
      if(!r.ok){let detail='';try{detail=(await r.json()).detail}catch{}throw new Error(String(detail||`Image service returned ${r.status}`))}
      const blob=await r.blob();
      setBackground(URL.createObjectURL(blob));setPosition(15);
    }catch(e){setError(e instanceof Error?e.message:String(e))}
    finally{setBusy(false)}
  };
  return <section aria-label="Teacher image generation and avatar overlay" style={{padding:16,border:'1px solid #b8cad6',borderRadius:12,margin:'12px 0'}}>
    <h3 style={{margin:'0 0 8px'}}>Reference-guided lesson artwork</h3>
    <p style={{fontSize:13}}>Upload a reference scene, generate a matching background, approve it, then preview the student avatar as a separate overlay.</p>
    <div style={{display:'flex',flexWrap:'wrap',gap:10,alignItems:'center',marginBottom:12}}>
      <label style={{fontSize:13}}>Reference image <input aria-label="Reference scene image" type="file" accept="image/png,image/jpeg,image/webp" onChange={e=>{setReference(e.target.files?.[0]??null);setApproved(false)}}/></label>
      <button type="button" onClick={generate} disabled={!reference||busy}>{busy?'Generating…':'Generate background'}</button>
      {background&&<button type="button" onClick={()=>setApproved(true)} disabled={approved}>{approved?'Approved ✓':'Approve artwork'}</button>}
    </div>
    {error&&<p role="alert" style={{color:'#b42318'}}>{error} — existing illustrated lesson remains available below.</p>}
    {background&&<div>
      <div style={{position:'relative',width:'100%',aspectRatio:'16 / 9',overflow:'hidden',borderRadius:10,background:'#dcebf3'}}>
        <img src={background} alt="AI-generated lesson background without the student avatar" style={{width:'100%',height:'100%',objectFit:'cover'}}/>
        {approved&&studentId&&<img src={`${API}/avatar/${encodeURIComponent(studentId)}/render.svg`} alt={`${studentName||'Student'} avatar overlay`} onError={e=>{e.currentTarget.style.display='none'}} style={{position:'absolute',left:`${position}%`,bottom:'9%',height:'30%',maxWidth:'25%',objectFit:'cover',objectPosition:'left',clipPath:'inset(0 50% 0 0)',transform:'scale(1.6)',transformOrigin:'bottom left',transition:reduceMotion?'none':'left 350ms ease'}}/>}
      </div>
      {approved?<div style={{marginTop:12}}>
        <label>Demo avatar position <input type="range" min="0" max="75" value={position} onChange={e=>setPosition(Number(e.target.value))}/></label>
        <label style={{marginLeft:12}}><input type="checkbox" checked={reduceMotion} onChange={e=>setReduceMotion(e.target.checked)}/> Reduce motion</label>
        {!studentId&&<p style={{fontSize:12}}>Select a backend student record with a saved avatar to show the overlay. Demo-only IDs like s1 cannot load it.</p>}
      </div>:<p style={{fontSize:12}}>Artwork awaits teacher approval. No student avatar shown yet.</p>}
    </div>}
    {!background&&<p style={{fontSize:12,color:'#60748a'}}>No generated image yet. The existing illustrated template remains below as fallback.</p>}
  </section>;
}
