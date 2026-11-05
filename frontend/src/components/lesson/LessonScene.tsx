import LessonAvatarSprite, { type LessonAvatarChoice } from './LessonAvatarSprite';
/**
 * File: LessonScene.tsx
 * Purpose: One continuous pixel-art scene at three visual detail levels.
 * Directed and reviewed by: Edenna Chen
 * AI-assisted implementation: ChatGPT (OpenAI), GPT-6, 2026-11-05
 * Adapted from the existing Fraction Fortress V3 mock SVG.
 * No image generation calls, network calls, persistence, or pet events.
 */
import type { CSSProperties } from 'react';
export type Complexity = 'Simple' | 'Moderate' | 'Rich';
/** Detailed, deterministic SVG tile scene. Reuses the same scenery at every stage. */
export default function LessonScene({ built, finale, complexity, avatar }: { built: number; finale: boolean; complexity: Complexity; avatar?: LessonAvatarChoice | null }) {
  const simple = complexity === 'Simple';
  const rich = complexity === 'Rich';
  const stones = Array.from({ length: 8 }, (_, i) => i);
  return <svg viewBox="0 0 800 390" role="img" aria-label={`Pixel-art fantasy valley with a fox, river and castle. ${built} of 8 bridge sections restored.`} style={{ display: 'block', width: '100%', borderRadius: 4, imageRendering: 'pixelated', background: simple ? '#faf7f0' : '#dcebf3' }}>
    <defs>
      <pattern id="grassTile" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="#7bc46e"/><path d="M7 31v-7m4 6v-4m18-12v-6m4 6v-3" stroke="#4b9957" strokeWidth="2"/><rect x="17" y="33" width="4" height="4" fill="#e7d67b"/></pattern>
      <pattern id="waterTile" width="64" height="35" patternUnits="userSpaceOnUse"><rect width="64" height="35" fill="#358ac0"/><path d="M4 12h23m15 13h19M8 29h10" stroke="#8bd9e8" strokeWidth="3"/><path d="M28 6h16" stroke="#226da7" strokeWidth="3"/></pattern>
      <pattern id="stoneTile" width="36" height="24" patternUnits="userSpaceOnUse"><rect width="36" height="24" fill="#b7b8c3"/><path d="M0 12h36M18 0v12M8 12v12M29 12v12" stroke="#83899d" strokeWidth="2"/></pattern>
    </defs>
    <rect width="800" height="390" fill={simple ? "#faf7f0" : "#dcebf3"}/>
    {simple ? <g>
      <rect x="0" y="300" width="198" height="90" fill="#c4d8b1"/>
      <rect x="535" y="300" width="265" height="90" fill="#c4d8b1"/>
      <rect x="198" y="306" width="337" height="84" fill="#b4d9e8"/>
      <rect x="198" y="301" width="337" height="6" fill="#86bbd1"/>
    </g> : <g opacity={rich ? 0.83 : 0.54}>
    <g fill="#f9f7e9"><rect x="82" y="40" width="108" height="20"/><rect x="108" y="22" width="57" height="20"/><rect x="540" y="45" width="120" height="19"/><rect x="562" y="29" width="74" height="18"/></g>
    <path d="M0 202 H42 V170 H70 V143 H95 V113 H119 V143 H145 V170 H181 V198 H220 V169 H246 V141 H271 V117 H295 V147 H324 V177 H354 V208 H438 V176 H459 V151 H480 V130 H504 V151 H533 V179 H561 V206 H664 V171 H685 V142 H704 V115 H727 V142 H750 V173 H778 V203 H800 V293 H0Z" fill="#8aaec0"/><path d="M0 229 H49 V206 H78 V177 H108 V153 H132 V180 H160 V204 H198 V228 H244 V199 H272 V172 H301 V151 H326 V180 H358 V206 H414 V235 H484 V205 H511 V182 H537 V163 H561 V185 H591 V207 H650 V229 H706 V201 H730 V174 H757 V151 H779 V174 H800 V182 V297 H0Z" fill="#608e9d"/>
    <rect x="0" y="239" width="800" height="151" fill="url(#grassTile)"/>
    <path d="M0 314 H90 V307 H170 V299 H235 V303 H322 V308 H418 V302 H515 V296 H610 V300 H710 V297 H800 V390 H0Z" fill="#5da855" opacity=".55"/>
    <path d="M190 258 H226 V250 H260 V241 H303 V235 H348 V241 H385 V249 H406 V255 H480 V258 H565 V251 H650 V253 H800 V390 H183 V281 H190Z" fill="url(#waterTile)"/>
    <path d="M188 260 H226 V252 H260 V243 H303 V237 H348 V243 H385 V251 H406 V259 H480 V262 H565 V255 H650 V257 H800" fill="none" stroke="#b5e9e4" strokeWidth="8"/>
    <path d="M187 375 H230 V366 H270 V358 H315 V352 H365 V356 H410 V366 H460 V375 H505 V379" fill="none" stroke="#b5e9e4" strokeWidth="7" opacity=".7"/>
    {/* Pine trees: layered triangular crowns and trunks */}
    {[35,91,155,615,738,782].map((x,i) => <g key={x} transform={`translate(${x} ${i%2?171:190})`}><rect x="-6" y="56" width="12" height="48" fill="#79513e"/><path d="M-8 0 H8 V17 H17 V33 H26 V49 H37 V65 H-37 V49 H-26 V33 H-17 V17 H-8Z" fill="#285d50"/><path d="M-9 19 H9 V35 H17 V50 H25 V65 H31 V79 H-31 V65 H-25 V50 H-17 V35 H-9Z" fill="#317c5b"/><path d="M-10 40 H10 V55 H19 V67 H28 V80 H36 V92 H-36 V80 H-28 V67 H-19 V55 H-10Z" fill="#236448"/><path d="M-10 48h12" stroke="#83b17a" strokeWidth="5"/></g>)}
    </g>}
    {/* Castle on the far shore */}
    <g transform="translate(515 104)" opacity={simple ? 1 : rich ? 0.94 : 0.8}>
      <rect x="36" y="66" width="202" height="135" fill={rich ? "url(#stoneTile)" : "#c2c1ca"} stroke="#616c84" strokeWidth="5"/>
      <rect x="5" y="34" width="67" height="167" fill={rich ? "url(#stoneTile)" : "#c2c1ca"} stroke="#616c84" strokeWidth="5"/>
      <rect x="200" y="34" width="67" height="167" fill={rich ? "url(#stoneTile)" : "#c2c1ca"} stroke="#616c84" strokeWidth="5"/>
      {!simple && [8,30,52,202,224,246].map(x => <rect key={x} x={x} y="14" width="18" height="31" fill="#707c94"/>)}
      {rich && [52,78,104,130,156,182,208].map(x => <rect key={x} x={x} y="50" width="18" height="27" fill="#7d889e"/>)}
      <path d="M109 201 V143 H115 V132 H122 V122 H132 V115 H143 V115 H153 V122 H160 V132 H165 V143 V201Z" fill="#433d50"/><path d="M136 119v82" stroke="#a17a55" strokeWidth="4"/>
      <rect x="25" y="88" width="20" height="36" fill="#354966"/><rect x="228" y="88" width="20" height="36" fill="#354966"/>
      <rect x="124" y="-15" width="5" height="72" fill="#665a5b"/><path d="M129 -15h57l-12 22h-45Z" fill="#e6a657"/>
    </g>
    {rich && <g opacity="0.75">
      {[55,110,160,610,690,760].map((x,i) => <g key={x}><rect x={x} y={337+i%2*16} width="12" height="5" fill="#d5a5ba"/><rect x={x+4} y={343+i%2*16} width="3" height="11" fill="#769e85"/></g>)}
      <rect x="650" y="195" width="22" height="7" fill="#e5e5d3"/>
      <rect x="678" y="201" width="15" height="7" fill="#e5e5d3"/>
    </g>}
    {/* Bridge supports and changing stone segments */}
    <rect x="185" y="304" width="350" height="18" fill="#534c52" opacity=".55"/>
    {stones.map(i => { const x=202+i*41; const active=i<built; return <g key={i}><rect x={x} y="275" width="38" height="34" fill={active?'#cda36d':'#8bb7c5'} opacity={active?1:.6} stroke={active?'#7d624d':'#d4eff0'} strokeWidth="3" strokeDasharray={active?'none':'5 5'}/>{active&&<><path d={`M${x+4} 284h30M${x+19} 284v20`} stroke="#efd3a0" strokeWidth="3"/><rect x={x+5} y="300" width="29" height="4" fill="#946f52"/></>}</g>; })}
    {/* Flowers and stones */}
    {rich && [29,68,125,168,548,590,707,763].map((x,i)=><g key={x}><rect x={x} y={345+i%3*11} width="7" height="5" fill={i%2?'#ffe6a2':'#f6b8d2'}/><rect x={x+3} y={350+i%3*11} width="2" height="9" fill="#326e48"/></g>)}
          {/* Separate full-body avatar layer; bridge/castle/river are unchanged. */}
      <g transform={`translate(${finale?560:107} 243)`}>
        <LessonAvatarSprite choice={avatar}/>
      </g>
    <rect x="17" y="15" width="267" height="38" fill="#1d3758" opacity=".88"/><text x="29" y="40" fill="#fff2d2" fontSize="20" fontWeight="bold">FRACTION FORTRESS</text>
    <rect x="17" y="60" width="160" height="27" fill="#fff5df"/><text x="29" y="79" fill="#30465d" fontSize="15" fontWeight="bold">Bridge: {built} / 8</text>
  </svg>;
}

