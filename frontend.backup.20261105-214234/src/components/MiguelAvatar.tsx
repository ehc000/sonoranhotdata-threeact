/** Miguel SVG presentation. No raster conversion, so the original portrait stays sharp.
 * Backend still stores a pet for compatibility; the frontend does not display it.
 * MUST TODO: restore VITE_API_URL through vite/client and shared API configuration.
 */
import { useEffect, useState } from 'react';
export const isUuid = (id: string) => /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(id);
const API = 'http://localhost:8000';
export function PixelAvatarImage({ src, size = 220, alt = 'Avatar' }: {src:string;size?:number;alt?:string;resolution?:number;hideCompanion?:boolean}) {
  const [markup, setMarkup] = useState('');
  const [error, setError] = useState(false);
  useEffect(() => {
    let active = true;
    setMarkup('');setError(false);
    fetch(src).then(r=>{if(!r.ok)throw new Error('Avatar unavailable');return r.text()}).then(svg=>{
      // Miguel's SVG viewBox is 200 x 100; left half is character, right half pet.
      // Crop using SVG viewBox, not bitmap resampling. Never inject remote SVG into DOM.
      const cropped = svg.replace(/viewBox="0 0 200 100"/, 'viewBox="0 0 100 100"');
      if(active) setMarkup('data:image/svg+xml;charset=utf-8,'+encodeURIComponent(cropped));
    }).catch(()=>{if(active)setError(true)});
    return ()=>{active=false};
  },[src]);
  if(error)return <div role="img" aria-label="Avatar unavailable">Avatar unavailable</div>;
  return <div style={{width:size,height:size,maxWidth:'100%',display:'grid',placeItems:'center'}}>
    {markup ? <img src={markup} alt={alt} width={size} height={size} style={{display:'block',objectFit:'contain'}}/> : <span aria-live="polite">Loading avatar…</span>}
  </div>;
}
export default function MiguelAvatar({studentId,size=180}:{studentId:string;size?:number}) {
 if(!isUuid(studentId))return <div role="img" aria-label="Avatar not configured" style={{width:size,minHeight:size/2,display:'grid',placeItems:'center',border:'1px dashed #83899d'}}>Avatar not set up</div>;
 return <PixelAvatarImage src={`${API}/avatar/${encodeURIComponent(studentId)}/render.svg`} size={size} alt="Your customized character"/>;
}
