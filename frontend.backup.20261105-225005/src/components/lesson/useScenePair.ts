import { useEffect, useState } from 'react';
import type { RenderableLesson } from './LessonRenderer';

type Phase = 'intro' | 'refresher' | 'question' | 'success' | 'finale';
type Pair = { before: string | null; after: string | null; loading: boolean; error: boolean };
const cached = new Map<string, string>();
const API = 'http://localhost:8000';
const fetchImage = async (payload: object, signal: AbortSignal): Promise<string> => {
  const response = await fetch(`${API}/api/lesson-scene-pairs/generate`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload), signal,
  });
  if (!response.ok) throw new Error(`Scene image HTTP ${response.status}`);
  return URL.createObjectURL(await response.blob());
};
export function useScenePair(lesson: RenderableLesson, phase: Phase, index: number): Pair {
  const questions = lesson.activities.flatMap(a => a.questions);
  const frame = phase === 'intro' || phase === 'refresher' ? 0 : phase === 'finale' ? questions.length + 1 : index + 1;
  const key = `${lesson.lesson_id}:${frame}`;
  const [state, setState] = useState<Pair>({ before: null, after: null, loading: true, error: false });
  useEffect(() => {
    let live = true;
    const controller = new AbortController();
    const beforeKey = `${key}:before`, afterKey = `${key}:after`;
    const initialBefore = cached.get(beforeKey) || null;
    const initialAfter = cached.get(afterKey) || null;
    setState({ before: initialBefore, after: initialAfter, loading: !initialAfter, error: false });
    if (initialAfter) return () => { live = false; controller.abort(); };
    const descriptions = [
      lesson.introduction,
      ...questions.map(q => q.before_visual_prompt || q.visual_prompt || q.narrative || q.text),
      lesson.conclusion,
    ];
    const payload = {
      lesson_id: lesson.lesson_id, story_title: lesson.story?.title || lesson.mission?.title || 'Lesson adventure',
      setting: [lesson.story?.story_goal, lesson.mission?.goal, lesson.objective].filter(Boolean).join('. ').slice(0, 1500),
      scene_number: frame, total_scenes: questions.length + 2,
      scene_description: descriptions[frame] || lesson.objective,
      previous_scene_description: frame > 0 ? descriptions[frame - 1] || '' : '',
    };
    (async () => {
      try {
        const before = initialBefore || await fetchImage({ ...payload, phase: 'before' }, controller.signal);
        if (!live) { if (!initialBefore) URL.revokeObjectURL(before); return; }
        cached.set(beforeKey, before);
        setState({ before, after: null, loading: true, error: false });
        const after = await fetchImage({ ...payload, phase: 'after' }, controller.signal);
        if (!live) { URL.revokeObjectURL(after); return; }
        cached.set(afterKey, after);
        setState({ before, after, loading: false, error: false });
      } catch {
        if (live) setState(s => ({ ...s, loading: false, error: true }));
      }
    })();
    return () => { live = false; controller.abort(); };
  }, [key]);
  return state;
}
