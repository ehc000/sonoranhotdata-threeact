/** AI-assisted editor UI. Preserves Miguel's catalog and PUT payload.
 * MUST TODO: restore configurable VITE_API_URL with proper vite/client types.
 * MUST TODO: persist optional companion visibility after agreeing on backend schema.
 */
import { useEffect, useState } from 'react';
import type { Student } from '../../types';
import MiguelAvatar, { PixelAvatarImage, isUuid } from '../../components/MiguelAvatar';
const API = 'http://localhost:8000';
type Catalog = { bases: string[]; heads: Record<string, string[]>; colors: string[]; color_names?: string[]; eyes: string[]; pets: string[] };
type AvatarData = { base: string; primary_color: string; head: string; eyes: string; display_name: string; static_mode: boolean };
type Preferences = { interests: string[]; content_format: 'text'|'images'|'audio'|'mixed'; sensory_sensitive: boolean; help_mode: 'offer'|'ask'; break_minutes: 2|5 };
const defaults: Preferences = { interests: [], content_format: 'mixed', sensory_sensitive: false, help_mode: 'offer', break_minutes: 2 };
const pretty = (s: string) => s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
const field: React.CSSProperties = { display: 'grid', gap: 5, fontWeight: 650, fontSize: 13, minWidth: 0 };
const control: React.CSSProperties = { width: '100%', boxSizing: 'border-box', minHeight: 40, padding: '7px 10px', border: '1px solid #cbd5df', borderRadius: 8, background: '#fff', color: '#24394d', fontSize: 14 };
export default function Avatar({ student, onUpdate: _onUpdate }: { student: Student; onUpdate: (changes: Partial<Student>) => void }) {
  const [catalog, setCatalog] = useState<Catalog | null>(null);
  const [avatar, setAvatar] = useState<AvatarData | null>(null);
  const [pet, setPet] = useState(''); // Required by Miguel backend; never displayed.
  const [preferences, setPreferences] = useState<Preferences>(defaults);
  const [message, setMessage] = useState('');
  const [savedVersion, setSavedVersion] = useState(0);
  useEffect(() => {
    let active = true;
    async function load() {
      try {
        const response = await fetch(`${API}/avatar/catalog`);
        if (!response.ok) throw new Error('Could not load avatar catalog');
        const c: Catalog = await response.json();
        if (!active) return;
        setCatalog(c);
        const firstBase = c.bases[0];
        setAvatar({ base: firstBase, primary_color: c.colors[0], head: c.heads[firstBase][0], eyes: c.eyes[0], display_name: '', static_mode: false });
        setPet(c.pets[0]);
        if (isUuid(student.id)) {
          const existing = await fetch(`${API}/avatar/${student.id}`);
          if (existing.ok) {
            const data = await existing.json();
            if (active) { setAvatar(data.avatar); setPet(data.pet.type); setPreferences(data.preferences); }
          } else if (existing.status !== 404) throw new Error('Could not load saved avatar');
        }
      } catch (error) { if (active) setMessage(String(error)); }
    }
    load();
    return () => { active = false; };
  }, [student.id]);
  async function save() {
    if (!avatar || !isUuid(student.id)) return;
    setMessage('Saving…');
    try {
      const response = await fetch(`${API}/avatar/${student.id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ avatar, pet_type: pet, preferences: { ...preferences, interests: preferences.interests.length ? preferences.interests : student.interests } }) });
      if (!response.ok) throw new Error(`Save failed (${response.status}): ${await response.text()}`);
      setSavedVersion(v => v + 1);
      setMessage('Avatar saved!');
    } catch (error) { setMessage(String(error)); }
  }
  // The standalone lesson demo reads this local-only preview. Backend records are unchanged.
  useEffect(() => { if (avatar) localStorage.setItem('sonoran-lesson-avatar-preview', JSON.stringify(avatar)); }, [avatar]);
  const preview = avatar && pet ? `${API}/avatar/preview.svg?${new URLSearchParams({ base: avatar.base, primary_color: avatar.primary_color, head: avatar.head, eyes: avatar.eyes, pet_type: pet })}` : '';
  return <div className="page narrow">
    <p className="eyebrow">MAKE IT YOURS</p><h1>Customize your avatar</h1>
    <p className="lead">Customize your character. Your full-body adventure sprite appears in lessons.</p>
    {!isUuid(student.id) && <p role="alert" style={{ padding: 10, background: '#fff4dd', borderRadius: 8, fontSize: 13 }}>Demo preview only: this student's ID isn't connected to Miguel's avatar records, so saving is disabled.</p>}
    {catalog && avatar ? <div className="card" style={{ display: 'grid', gap: 14, padding: 18 }}>
      <label style={field}>Avatar name<input style={control} maxLength={20} placeholder="Give your character a name" value={avatar.display_name} onChange={e => setAvatar({ ...avatar, display_name: e.target.value })} /></label>
      <div style={{ display: 'grid', placeItems: 'center', gap: 8, padding: '14px 8px', border: '1px solid #d7e1e8', background: '#eef4f7', borderRadius: 12 }}>
        <PixelAvatarImage src={preview} alt="Live sharp character preview" size={220} />
        <span style={{ fontSize: 12, color: '#4c6376' }}>Live preview · original sharp SVG</span>
      </div>
      <div style={{ padding: 10, background: '#f1f5f9', borderRadius: 10, fontSize: 12, color: '#42556a' }}>The lesson uses a separate full-body pixel sprite based on these choices. This editor keeps Miguel's original sharp portrait.</div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(155px, 1fr))', gap: 12 }}>
        <label style={field}>Character type<select style={control} value={avatar.base} onChange={e => { const base = e.target.value; setAvatar({ ...avatar, base, head: catalog.heads[base][0] }); }}>{catalog.bases.map(x => <option key={x} value={x}>{pretty(x)}</option>)}</select></label>
        <label style={field}>Head<select style={control} value={avatar.head} onChange={e => setAvatar({ ...avatar, head: e.target.value })}>{catalog.heads[avatar.base].map(x => <option key={x} value={x}>{pretty(x.replace(`${avatar.base}_`, ''))}</option>)}</select></label>
        <label style={field}>Eyes<select style={control} value={avatar.eyes} onChange={e => setAvatar({ ...avatar, eyes: e.target.value })}>{catalog.eyes.map(x => <option key={x} value={x}>{pretty(x)}</option>)}</select></label>
      </div>
      <div style={{ display: 'grid', gap: 7 }}><span style={{ fontWeight: 650, fontSize: 13 }}>Character color</span>
        <div role="group" aria-label="Character color" style={{ display: 'flex', gap: 9, flexWrap: 'wrap' }}>{catalog.colors.map((color, i) => <button key={color} type="button" onClick={() => setAvatar({ ...avatar, primary_color: color })} aria-label={`${catalog.color_names?.[i] || color} color`} aria-pressed={avatar.primary_color.toUpperCase() === color.toUpperCase()} title={catalog.color_names?.[i] || color} style={{ width: 37, height: 37, borderRadius: 8, background: color, border: avatar.primary_color.toUpperCase() === color.toUpperCase() ? '3px solid #24394d' : '2px solid #fff', outline: avatar.primary_color.toUpperCase() === color.toUpperCase() ? '2px solid #88a4b8' : '1px solid #aebdc8', cursor: 'pointer' }} />)}</div>
      </div>
      <label style={{ display: 'flex', alignItems: 'center', gap: 12, background: '#e9f2f8', border: '1px solid #b7cedc', padding: 13, borderRadius: 10, cursor: 'pointer' }}>
        <input type="checkbox" aria-label="Reduce motion" checked={avatar.static_mode} onChange={e => setAvatar({ ...avatar, static_mode: e.target.checked })} style={{ width: 20, height: 20, accentColor: '#285a80', flexShrink: 0 }} />
        <span><strong style={{ display: 'block' }}>Reduce motion</strong><span style={{ fontSize: 12, color: '#476275' }}>Prefer a still character without animations. This setting will also apply when motion is added later.</span></span>
      </label>
      <button className="btn primary" disabled={!isUuid(student.id)} onClick={save}>Save avatar</button>
      {savedVersion > 0 && <div><p>Saved avatar</p><MiguelAvatar key={savedVersion} studentId={student.id} size={260} /></div>}
    </div> : <p>Loading avatar options…</p>}
    {message && <p role="status">{message}</p>}
  </div>;
}
