/** Original handheld-RPG-inspired full-body sprites. No imported game artwork.
 * Every catalog head option has its own visible silhouette or defining features.
 * 40x52 native grid enlarged 2x; no rasterization, blur or pet.
 */
export type LessonAvatarChoice = {base:string;head:string;eyes:string;primary_color:string;static_mode?:boolean};
type Tile={x:number;y:number;w:number;h:number;fill:string};
export default function LessonAvatarSprite({choice}:{choice?:LessonAvatarChoice|null}) {
 const base=choice?.base??'human', head=choice?.head??'human_round', eyes=choice?.eyes??'dots';
 const color=/^#[0-9a-f]{6}$/i.test(choice?.primary_color??'')?choice!.primary_color:'#A8C5DA';
 const tone=(f:number)=>{const n=parseInt(color.slice(1),16);return '#'+[n>>16,(n>>8)&255,n&255].map(c=>Math.max(0,Math.min(255,Math.round(c*f))).toString(16).padStart(2,'0')).join('')};
 const ink='#394254', dark=tone(.76), bright=tone(1.17), skin=color;
 const p:Tile[]=[];const r=(x:number,y:number,w:number,h:number,fill:string)=>p.push({x,y,w,h,fill});
 // Short, athletic game-sprite proportions: neck, jacket, two arms, trousers and boots.
 r(13,27,15,3,ink);r(14,27,13,3,skin);
 r(8,30,25,15,ink);r(10,31,21,12,'#537a9b');r(11,32,19,2,'#88a9bf');
 r(8,31,5,13,ink);r(9,32,3,10,skin);r(29,31,5,13,ink);r(30,32,3,10,skin);
 r(9,42,4,3,dark);r(30,42,4,3,dark);
 r(18,32,3,11,'#d9bd87');r(10,41,21,3,'#364d70');r(17,42,7,2,'#d6ae6f');
 r(12,44,8,5,ink);r(22,44,8,5,ink);r(13,44,6,4,'#3d526f');r(23,44,6,4,'#3d526f');
 r(10,48,11,4,ink);r(21,48,11,4,ink);r(11,49,9,2,'#896650');r(22,49,9,2,'#896650');
 // Head variants use DISTINCT silhouettes. Draw outline first, then fill inset.
 const variant=head.split('_').slice(1).join('_');
 const oval=variant==='oval', square=variant==='square', soft=variant==='soft';
 if(base==='human'){
   if(square){r(9,7,24,22,ink);r(10,8,22,20,skin);}
   else if(oval){r(14,4,14,3,ink);r(10,7,22,18,ink);r(14,25,14,4,ink);r(12,8,18,17,skin);r(15,25,12,2,skin);}
   else if(soft){r(12,6,18,3,ink);r(9,9,24,14,ink);r(12,23,18,5,ink);r(11,10,20,14,skin);r(13,24,16,2,skin);}
   else {r(13,5,16,3,ink);r(9,8,24,16,ink);r(13,24,16,4,ink);r(11,9,20,15,skin);r(14,24,14,2,skin);}
   // Distinct hair silhouettes: oval side part, square flat top, soft swoop, round fringe.
   if(square){r(10,8,22,5,'#57443e');r(10,13,4,4,'#57443e');}
   else if(oval){r(12,7,17,5,'#57443e');r(12,12,3,5,'#57443e');r(24,8,6,2,'#57443e');}
   else if(soft){r(12,8,17,4,'#57443e');r(9,11,9,4,'#57443e');r(17,11,5,2,'#57443e');}
   else {r(13,7,16,5,'#57443e');r(10,10,8,4,'#57443e');r(25,10,6,3,'#57443e');}
 } else if(base==='animal'){
   if(variant==='rabbit'){r(11,0,7,14,ink);r(12,1,5,12,color);r(14,3,2,8,'#e6a6a8');r(24,0,7,14,ink);r(25,1,5,12,color);r(27,3,2,8,'#e6a6a8');}
   if(variant==='cat'){r(8,5,11,11,ink);r(10,7,8,9,color);r(23,5,11,11,ink);r(24,7,8,9,color);r(12,8,3,4,'#e6a6a8');r(27,8,3,4,'#e6a6a8');}
   if(variant==='dog'){r(5,12,8,16,ink);r(6,13,6,13,dark);r(29,12,8,16,ink);r(30,13,6,13,dark);}
   if(variant==='bear'){r(8,7,10,10,ink);r(10,9,6,6,color);r(24,7,10,10,ink);r(26,9,6,6,color);}
   r(11,11,20,16,ink);r(12,12,18,14,color);r(14,13,14,3,bright);
   r(16,22,10,5,bright);r(19,22,4,3,'#77575a');
 } else if(base==='robot'){
   if(variant==='dome'){r(14,6,14,3,ink);r(10,9,22,4,ink);r(8,13,26,14,ink);r(10,14,22,11,color);r(12,10,18,4,bright);}
   else if(square){r(8,8,26,20,ink);r(9,9,24,18,color);r(10,10,22,3,bright);}
   else if(oval){r(14,6,14,3,ink);r(10,9,22,17,ink);r(14,26,14,3,ink);r(12,10,18,16,color);r(15,26,12,1,color);}
   else {r(12,7,18,3,ink);r(8,10,26,15,ink);r(12,25,18,3,ink);r(10,11,22,14,color);r(13,25,16,1,color);}
   r(19,3,4,5,ink);r(20,1,2,3,'#edc46f');r(12,14,18,10,'#b8d4db');r(13,15,16,8,'#d9e7e9');
 } else {
   if(variant==='horned'){r(10,3,7,12,ink);r(11,4,5,10,'#e8c98b');r(25,3,7,12,ink);r(26,4,5,10,'#e8c98b');}
   if(variant==='fuzzy'){for(let x=9;x<34;x+=6)r(x,7-(x%3),4,7,ink);}
   if(variant==='finned'){r(5,12,8,13,ink);r(6,13,6,11,dark);r(29,12,8,13,ink);r(30,13,6,11,dark);}
   if(variant==='blob'){r(14,5,14,4,ink);r(9,9,24,17,ink);r(13,26,16,3,ink);r(11,10,20,16,color);r(14,26,14,1,color);}
   else {r(11,10,20,18,ink);r(12,11,18,16,color);}
   r(14,12,14,3,bright);
 }
 // Eye selections are intentionally exaggerated to be visible at lesson scale.
 const eyeInk=base==='robot'?'#305571':'#293447';
 if(eyes==='wide'){for(const x of [14,24]){r(x,17,6,6,'#fff4e8');r(x+2,18,3,4,eyeInk);r(x+2,18,1,1,'#fff');}}
 else if(eyes==='round'){for(const x of [15,25]){r(x,17,5,5,eyeInk);r(x+1,17,2,2,'#fff');}}
 else if(eyes==='soft_curve'){for(const x of [14,24]){r(x,19,6,2,eyeInk);r(x+1,18,4,1,eyeInk);}}
 else {r(16,18,3,3,eyeInk);r(26,18,3,3,eyeInk);}
 if(base==='human'||base==='creature')r(20,24,3,1,'#9c6869');
 if(base==='robot')r(19,24,5,2,'#537e91');
 // scarf drawn on top of neck, but not over facial features
 r(12,28,19,3,'#a5485c');r(14,28,15,1,'#e07c85');r(27,30,4,7,'#a5485c');
 return <g shapeRendering="crispEdges" transform="translate(0 -8) scale(2)" aria-label={`${head} full-body pixel adventurer`}>
 {p.map((t,i)=><rect key={i} x={t.x} y={t.y} width={t.w} height={t.h} fill={t.fill}/>)}
 </g>;
}
