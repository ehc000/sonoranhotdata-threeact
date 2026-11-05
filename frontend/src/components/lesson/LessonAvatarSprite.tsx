/** AI-assisted full-body lesson sprite, matching Fraction Fortress stepped SVG art.
 * Uses Miguel's base/head/eye/color choices; does not modify Miguel's backend.
 */
export type LessonAvatarChoice = {base:string;head:string;eyes:string;primary_color:string;static_mode?:boolean};
export default function LessonAvatarSprite({choice}:{choice?:LessonAvatarChoice|null}) {
 const base=choice?.base ?? 'animal'; const head=choice?.head ?? 'animal_cat';
 const color=choice?.primary_color ?? '#db8546'; const dark='#354966';
 const animal=base==='animal';const robot=base==='robot';const creature=base==='creature';
 const ears=animal ? (head.includes('rabbit') ? 27 : 15) : creature ? 13 : 0;
 return <g shapeRendering="crispEdges">
   {/* 80x110 full-body sprite, aligned to original fox footprint */}
   <rect x="20" y="83" width="19" height="13" fill="#523f46"/><rect x="42" y="83" width="20" height="13" fill="#523f46"/>
   <rect x="22" y="61" width="17" height="25" fill={dark}/><rect x="43" y="61" width="17" height="25" fill={dark}/>
   <rect x="15" y="34" width="50" height="32" fill="#436f9b" stroke="#2f4c6e" strokeWidth="4"/>
   <rect x="7" y="41" width="9" height="26" fill={color}/><rect x="65" y="41" width="9" height="26" fill={color}/>
   {ears>0&&<><rect x="17" y={5-ears} width="13" height={ears+8} fill={color}/><rect x="50" y={5-ears} width="13" height={ears+8} fill={color}/></>}
   {robot?<><rect x="16" y="1" width="48" height="35" fill={color} stroke={dark} strokeWidth="4"/><rect x="35" y="-7" width="8" height="8" fill={dark}/></>:
   <><path d={head.includes('square')?'M14 3H65V36H14Z':'M22 0H58V6H66V30H60V37H20V30H13V8H22Z'} fill={color} stroke="#755b59" strokeWidth="3"/></>}
   {choice?.eyes==='wide'?<><rect x="24" y="14" width="10" height="10" fill="#f8f6e8"/><rect x="46" y="14" width="10" height="10" fill="#f8f6e8"/></>:null}
   <rect x="27" y="17" width={choice?.eyes==='round'?7:5} height="6" fill="#283d49"/><rect x="49" y="17" width={choice?.eyes==='round'?7:5} height="6" fill="#283d49"/>
   {!robot&&<rect x="37" y="27" width="7" height="4" fill="#493c3d"/>}
   <rect x="17" y="36" width="47" height="9" fill="#c94656"/><rect x="51" y="44" width="9" height="16" fill="#c94656"/>
   <rect x="54" y="53" width="16" height="14" fill="#a97948" stroke="#72583f" strokeWidth="3"/>
 </g>;
}
