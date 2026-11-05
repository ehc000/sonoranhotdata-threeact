from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
f=root/'frontend/src/components/lesson/LessonRenderer.tsx'
if not f.exists():raise SystemExit('Missing LessonRenderer.tsx. No changes made.')
s=f.read_text()
if 'SONORAN_ILLUSTRATED_PREVIEW_V1' in s:raise SystemExit('Already installed.')
anchor='<p className="eyebrow">MISSION LESSON · DEMO RENDERING</p>'
if anchor not in s:raise SystemExit('Renderer version differs; no changes made. Send LessonRenderer.tsx for exact patch.')
shutil.copy2(f,f.with_suffix('.tsx.before-illustrations.bak'))
s=s.replace(anchor,anchor+'\n      <SonoranIllustratedPreview lesson={lesson} />',1)
s+='''

/** SONORAN_ILLUSTRATED_PREVIEW_V1
 * Instant offline illustration template for teacher lesson previews.
 * Uses the assembled lesson text to select a scene; NOT generative AI imagery.
 * No external services, tokens, or changes to assessment / teacher approval.
 */
function SonoranIllustratedPreview({lesson}:{lesson:unknown}) {
  const text=JSON.stringify(lesson).toLowerCase();
  const space=/space|planet|astronaut|rocket|orbit|moon|star/.test(text);
  const nature=/plant|forest|tree|animal|biology|ecosystem|flower/.test(text);
  const math=/fraction|bridge|castle|geometry|number|mathematics/.test(text);
  const title=space?'Space expedition':nature?'Nature exploration':math?'Math adventure':'Learning adventure';
  return <figure style={{margin:'14px 0 22px',borderRadius:14,overflow:'hidden',border:'1px solid #b8cad6',background:'#dcebf3'}}>
    <svg viewBox="0 0 760 285" role="img" aria-label={`${title} illustrated lesson scene`} style={{display:'block',width:'100%',imageRendering:'pixelated'}}>
      <rect width="760" height="285" fill={space?'#263453':nature?'#cce9d5':'#dcebf3'}/>
      {space?<>
        {Array.from({length:24},(_,i)=><rect key={i} x={(i*137+29)%750} y={(i*53+17)%190} width={i%3+2} height={i%3+2} fill="#fff3b9"/>)}
        <circle cx="590" cy="84" r="55" fill="#f3dca7"/><circle cx="570" cy="67" r="12" fill="#d9bb89"/>
        <path d="M0 240Q170 180 350 240T760 210V285H0Z" fill="#967fbb"/>
        <path d="M150 212L195 135L239 212Z" fill="#e4eaf0" stroke="#4b567d" strokeWidth="7"/>
        <rect x="185" y="165" width="20" height="43" fill="#e09c77"/><path d="M150 212L132 231L165 217ZM239 212L259 231L224 217Z" fill="#e8ad72"/>
      </>:nature?<>
        <path d="M0 212Q200 150 370 212T760 205V285H0Z" fill="#78b98c"/>
        {[80,245,505,660].map((x,i)=><g key={x}><rect x={x-9} y={135+i%2*25} width="18" height="105" fill="#84644e"/><path d={`M${x-63} ${165+i%2*25}L${x} ${48+i%2*25}L${x+63} ${165+i%2*25}Z`} fill="#347c65"/><path d={`M${x-48} ${133+i%2*25}L${x} ${58+i%2*25}L${x+48} ${133+i%2*25}Z`} fill="#4c9a73"/></g>)}
        <path d="M320 285Q390 220 460 285Z" fill="#e6c9a1"/>
      </>:<>
        <path d="M0 210H760V285H0Z" fill="#7bc46e"/>
        <path d="M0 254H760V285H0Z" fill="#358ac0"/>
        <path d="M65 206L125 92L185 206ZM230 206L294 115L357 206Z" fill="#8aaec0"/>
        <rect x="550" y="103" width="135" height="118" fill="#c2c1ca" stroke="#616c84" strokeWidth="6"/>
        <rect x="531" y="83" width="35" height="138" fill="#a5a7b8" stroke="#616c84" strokeWidth="5"/>
        <rect x="671" y="83" width="35" height="138" fill="#a5a7b8" stroke="#616c84" strokeWidth="5"/>
        <path d="M604 221V177Q618 146 635 177V221Z" fill="#465066"/>
        {Array.from({length:7},(_,i)=><rect key={i} x={193+i*45} y="234" width="41" height="20" fill="#d4ad7c" stroke="#82694d" strokeWidth="3"/>)}
      </>}
      <rect x="20" y="18" width="330" height="43" rx="7" fill="#243b58" opacity=".93"/>
      <text x="34" y="47" fill="#fff3d7" fontSize="22" fontWeight="bold">{title.toUpperCase()}</text>
    </svg>
    <figcaption style={{padding:'9px 13px',fontSize:12,color:'#40556b',background:'#f8fafc'}}>Illustrated template selected from lesson content · AI image generation not yet connected</figcaption>
  </figure>;
}
'''
f.write_text(s)
print('Illustrated preview installed. Backup:',f.with_suffix('.tsx.before-illustrations.bak'))
