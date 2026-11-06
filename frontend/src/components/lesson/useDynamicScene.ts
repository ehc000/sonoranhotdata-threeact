import { useEffect, useState } from 'react';
import type { RenderableLesson } from './LessonRenderer';

type Phase = 'intro' | 'refresher' | 'question' | 'success' | 'finale';
const cache = new Map<string, string>();

export function useDynamicScene(lesson: RenderableLesson, phase: Phase, index: number) {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [status, setStatus] = useState<'loading' | 'ready' | 'fallback'>('loading');
  const questions = lesson.activities.flatMap(a => a.questions);
  const descriptions = [lesson.introduction, ...questions.map(q => q.before_visual_prompt || q.visual_prompt || q.narrative || q.text), lesson.conclusion];
  const frame = phase === 'intro' || phase === 'refresher' ? 0 : phase === 'finale' ? questions.length + 1 : index + 1;
  const key = `${lesson.lesson_id}:${frame}`;
  useEffect(() => {
    let cancelled = false;
    const saved = cache.get(key);
    if (saved) { setImageUrl(saved); setStatus('ready'); return; }
    setImageUrl(null); setStatus('loading');
    const payload = {
      lesson_id: lesson.lesson_id,
      story_title: lesson.story?.title || lesson.mission?.title || 'Lesson adventure',
      setting: [lesson.story?.story_goal, lesson.mission?.goal, lesson.objective].filter(Boolean).join('. ').slice(0, 1500),
      stage: phase,
      scene_number: frame,
      total_scenes: questions.length + 2,
      scene_description: descriptions[frame] || lesson.objective,
      previous_scene_description: frame > 0 ? descriptions[frame - 1] || '' : '',
    };
    const controller = new AbortController();
    fetch('http://localhost:8000/api/lesson-scenes/generate', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload), signal: controller.signal,
    }).then(async r => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.blob();
    }).then(blob => {
      const url = URL.createObjectURL(blob);
      if (cancelled) { URL.revokeObjectURL(url); return; }
      cache.set(key, url); setImageUrl(url); setStatus('ready');
    }).catch(() => { if (!cancelled) { setImageUrl(null); setStatus('fallback'); } });
    return () => { cancelled = true; controller.abort(); };
  }, [key]);
  return { imageUrl, status };
}
