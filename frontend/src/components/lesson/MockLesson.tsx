import type { LessonAvatarChoice } from './LessonAvatarSprite';
/**
 * Purpose: Standalone Fraction Fortress visual lesson preview (v4).
 * Directed and reviewed by: Edenna Chen
 * AI-assisted implementation: ChatGPT (OpenAI), GPT-6, 2026-11-05.
 * Original project components and Miguel's avatar work are not modified.
 * No external assets, API calls, grading, database writes, or pet-growth events.
 * V4: JSON-driven copy and shared three-level scene; preserves the existing UI flow.
 * Language selection changes narrative and visual detail, never math or answer choices.
 */
import { useState } from 'react';

import LessonScene from './LessonScene';
import lesson from './mockLesson.json';
import type { Complexity } from './LessonScene';

const buttonStyle: React.CSSProperties = { padding: '11px 17px', border: '2px solid #627895', borderRadius: 10, background: '#fff', color: '#1b3551', fontWeight: 700, cursor: 'pointer', fontSize: 15 };

export default function MockLesson() {
  const [lessonAvatar] = useState<LessonAvatarChoice | null>(() => { try { const raw=localStorage.getItem('sonoran-lesson-avatar-preview'); return raw ? JSON.parse(raw) as LessonAvatarChoice : null; } catch { return null; } });
  const [complexity, setComplexity] = useState<Complexity>('Moderate');
  const [stage, setStage] = useState<Stage>('intro');
  const [index, setIndex] = useState(0);
  const [choice, setChoice] = useState('');
  const [help, setHelp] = useState(false);
  const [built, setBuilt] = useState(0);
  const question = lesson.questions[index];
  const reset = () => { setStage('intro'); setIndex(0); setChoice(''); setHelp(false); setBuilt(0); };
  const next = () => { setChoice(''); setHelp(false); if (index < lesson.questions.length-1) { setIndex(index+1); setStage('challenge'); } else setStage('finale'); };
  return <main style={{ maxWidth: 850, margin: '24px auto', padding: '16px', fontFamily: 'system-ui, sans-serif', color: '#22364d' }}>
    <p style={{ fontSize: 12, fontWeight: 800, letterSpacing: 1.4 }}>STANDALONE DEMO · NO SAVED PROGRESS</p>
    <h1 style={{ marginBottom: 8 }}>Fraction Fortress</h1>
    <div style={{ display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap', marginBottom: 15 }}>
      <label htmlFor="story-complexity" style={{ fontWeight: 700 }}>Story language and visuals</label>
      <select id="story-complexity" value={complexity} onChange={e=>setComplexity(e.target.value as Complexity)} style={{ padding: '9px 12px', borderRadius: 8, border: '1px solid #7c8b9f', fontSize: 15 }}>
        <option>Simple</option><option>Moderate</option><option>Rich</option>
      </select>
      <span style={{ fontSize: 13, color: '#53677d' }}>Same math questions and bridge progress in all modes</span>
    </div>
    <LessonScene built={built} finale={stage==='finale'} complexity={complexity} avatar={lessonAvatar}/>
    <section style={{ background: '#f1f5f9', border: '1px solid #d5e0e9', borderRadius: 14, padding: 22, marginTop: 16 }}>
      {stage==='intro' && <><h2>Your mission</h2><p>{lesson.story.intro[complexity]}</p><button style={buttonStyle} onClick={()=>setStage('refresher')}>Start mission →</button></>}
      {stage==='refresher' && <><h2>Quick refresher</h2><p>{lesson.story.refresher[complexity]}</p><button style={buttonStyle} onClick={()=>setStage('challenge')}>Try a challenge →</button></>}
      {stage==='challenge' && <><p style={{ fontWeight: 800, fontSize: 13 }}>CHALLENGE {index+1} OF {lesson.questions.length}</p><p style={{ lineHeight: 1.55, marginBottom: 8 }}>{question.narrative[complexity]}</p><h2>{question.prompt}</h2><div style={{ display:'flex', flexWrap:'wrap', gap:10 }}>{question.options.map(option=><button key={option} aria-pressed={choice===option} onClick={()=>setChoice(option)} style={{ ...buttonStyle, background:choice===option?'#d8e9ff':'#fff', borderColor:choice===option?'#2b68a2':'#627895' }}>{option} stones</button>)}</div><div style={{ display:'flex', flexWrap:'wrap', gap:10, marginTop:18 }}><button style={buttonStyle} onClick={()=>setHelp(!help)}>{help?'Hide hint':'Need a hint?'}</button><button style={{...buttonStyle, opacity:choice?1:.5}} disabled={!choice} onClick={()=>{setBuilt(question.bridge_sections_after);setStage('success');}}>Place bridge stones →</button></div>{help&&<p role="status" style={{ padding:12, background:'#fff3c9', borderRadius:8 }}>{question.hint}</p>}<p style={{fontSize:12,color:'#526477'}}>Preview only: any selected answer advances; no grading is performed.</p></>}
      {stage==='success' && <><h2>Bridge progress!</h2><p>{lesson.story.success[complexity]}</p><button style={buttonStyle} onClick={next}>{index<lesson.questions.length-1?'Next challenge →':'Finish mission →'}</button></>}
      {stage==='finale' && <><h2>🏆 Mission complete!</h2><p>{lesson.story.finale[complexity]}</p><button style={buttonStyle} onClick={reset}>Replay lesson ↺</button></>}
    </section>
  </main>;
}
