/**
 * Purpose: Standalone mock lesson renderer for Fraction Fortress.
 *
 * Original application: Sonoran Hot Data adaptive classroom project.
 * New implementation: Hardcoded lesson preview with pixel-art visuals,
 * fraction challenges, story progression, and simulated completion.
 *
 * Directed and reviewed by: Edenna Chen
 * Code generated with assistance from: ChatGPT (OpenAI), GPT-6
 * Date: 2026-11-05
 *
 * Human edits: To be updated as the team modifies this component.
 * External sources: None.
 *
 * Notes:
 * - Uses mock lesson content; no LLM API calls.
 * - Does not modify student mastery, completion, or database records.
 * - Does not trigger pet-growth events.
 * - Intended for testing the renderer before generated story integration.
 */

import { useState } from 'react';

type Stage = 'intro' | 'refresher' | 'challenge' | 'success' | 'finale';
const questions = [
  { prompt: 'The bridge has 8 blocks. You need 1/2 of them to cross. How many blocks is that?', options: ['2', '4', '6'], answer: '4', hint: 'Half means splitting into two equal groups. 8 ÷ 2 = ?' },
  { prompt: 'The next bridge has 12 blocks. You need 1/4 of them. How many blocks?', options: ['3', '4', '6'], answer: '3', hint: 'One quarter means one of four equal groups. 12 ÷ 4 = ?' },
];

function Scene({ built, name }: { built: number; name: string }) {
  return <svg viewBox="0 0 640 280" role="img" aria-label={`Pixel-art castle scene. ${built} bridge segments repaired.`} style={{ width: '100%', maxHeight: 320, imageRendering: 'pixelated', borderRadius: 12, background: '#a9d9f5' }}>
    <rect x="0" y="182" width="640" height="98" fill="#8fca83" />
    <rect x="0" y="222" width="640" height="58" fill="#59b6d8" />
    <rect x="468" y="80" width="120" height="126" fill="#8b8da9" /><rect x="448" y="62" width="160" height="24" fill="#666b8e" />
    {[460, 494, 528, 562, 596].map(x => <rect key={x} x={x} y="45" width="19" height="28" fill="#666b8e" />)}
    <rect x="518" y="146" width="34" height="60" rx="16" fill="#3b425d" />
    <rect x="34" y="177" width="165" height="46" fill="#68a760" />
    {Array.from({length: 8}, (_, i) => <rect key={i} x={196 + i * 33} y="195" width="30" height="22" fill={i < built ? '#c89962' : '#d7edf4'} stroke={i < built ? '#8d623f' : '#91c5d9'} strokeWidth="3" />)}
    <g transform="translate(112 126)">
      <rect x="14" y="0" width="38" height="38" fill="#df9154" /><rect x="4" y="-11" width="20" height="23" fill="#df9154" /><rect x="42" y="-11" width="20" height="23" fill="#df9154" />
      <rect x="21" y="13" width="7" height="7" fill="#28283a" /><rect x="41" y="13" width="7" height="7" fill="#28283a" />
      <rect x="20" y="38" width="28" height="35" fill="#427eb6" /><rect x="20" y="70" width="10" height="19" fill="#41415a" /><rect x="38" y="70" width="10" height="19" fill="#41415a" />
    </g>
    <text x="145" y="118" textAnchor="middle" fontSize="16" fontWeight="bold" fill="#25354b">{name}</text>
    <text x="24" y="30" fontSize="16" fontWeight="bold" fill="#25354b">The Fraction Fortress</text>
  </svg>;
}

export default function MockLesson() {
  const [stage, setStage] = useState<Stage>('intro');
  const [index, setIndex] = useState(0);
  const [choice, setChoice] = useState('');
  const [help, setHelp] = useState(false);
  const [built, setBuilt] = useState(0);
  const question = questions[index];
  const btn = { padding: '10px 16px', borderRadius: 9, border: '1px solid #b5bdca', cursor: 'pointer', background: '#fff', fontSize: 15 } as const;
  const next = () => { setChoice(''); setHelp(false); if (index + 1 < questions.length) { setIndex(index + 1); setStage('challenge'); } else setStage('finale'); };
  return <main style={{ maxWidth: 760, margin: '24px auto', padding: 20, fontFamily: 'system-ui, sans-serif', color: '#24344d' }}>
    <p style={{ letterSpacing: 2, fontSize: 12, fontWeight: 700 }}>TEACHER PREVIEW · MOCK DATA ONLY</p>
    <h1>Fraction Fortress</h1>
    <Scene built={built} name="Alex" />
    <section style={{ background: '#f5f7fb', borderRadius: 14, padding: 22, marginTop: 18 }}>
      {stage === 'intro' && <><h2>Your mission</h2><p>Alex the fox needs your help to repair the bridge and reach the castle! Each fraction problem restores a part of the bridge.</p><button style={btn} onClick={() => setStage('refresher')}>Start mission →</button></>}
      {stage === 'refresher' && <><h2>Quick refresher</h2><p>A fraction tells us how many equal parts of a whole we want. To find <strong>1/2 of 8</strong>, split 8 into 2 equal groups.</p><button style={btn} onClick={() => setStage('challenge')}>Try a challenge →</button></>}
      {stage === 'challenge' && <><p>CHALLENGE {index + 1} OF {questions.length}</p><h2>{question.prompt}</h2><div style={{ display: 'flex', flexWrap: 'wrap', gap: 10 }}>{question.options.map(option => <button key={option} style={{ ...btn, background: choice === option ? '#d9eaff' : '#fff', borderColor: choice === option ? '#3676b8' : '#b5bdca' }} onClick={() => setChoice(option)}>{option} blocks</button>)}</div><div style={{ display: 'flex', gap: 10, marginTop: 18 }}><button style={btn} onClick={() => setHelp(!help)}>{help ? 'Hide hint' : 'Need a hint?'}</button><button style={btn} disabled={!choice} onClick={() => { setBuilt((index + 1) * 4); setStage('success'); }}>Continue →</button></div>{help && <p role="status" style={{ padding: 12, background: '#fff6d9', borderRadius: 8 }}>{question.hint}</p>}<p style={{ fontSize: 12, opacity: .75 }}>Demo only: selecting an answer advances without grading.</p></>}
      {stage === 'success' && <><h2>Bridge progress!</h2><p>Alex places more blocks on the bridge. You're getting closer to the fortress.</p><button style={btn} onClick={next}>{index + 1 < questions.length ? 'Next challenge →' : 'Finish mission →'}</button></>}
      {stage === 'finale' && <><h2>🏆 Mission complete!</h2><p>The bridge is repaired and Alex reaches the fortress. Great teamwork!</p><button style={btn} onClick={() => { setStage('intro'); setIndex(0); setBuilt(0); setChoice(''); setHelp(false); }}>Replay demo ↺</button></>}
    </section>
  </main>;
}
