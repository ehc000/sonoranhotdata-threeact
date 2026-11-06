import TeacherLessonPlayer from './TeacherLessonPlayer';
/**
 * File: LessonRenderer.tsx
 * Purpose: Render assembled mission lessons with local, simulated progress tracking.
 * Directed by: Edenna Chen
 * AI-assisted implementation: ChatGPT (OpenAI), GPT-6, 2026-11-05
 * Human review: Pending
 * Notes: No persistence, assignment, answer verification, or mastery updates.
 */
export type LessonQuestion = {
  question_id: string;
  text: string;
  story_dialogue?: string;
  narrative?: string;
  challenge_transition?: string;
  optional_reminder?: string;
  optional_walkthrough?: string[];
  story_bridge?: string;
  success_event?: string;
  mission_task_title?: string;
  mission_task_purpose?: string;
  before_visual_prompt?: string;
  after_visual_prompt?: string;
  visual_prompt?: string;
};

export type RenderableLesson = {
  lesson_id: string;
  objective: string;
  story: { title: string; story_goal?: string };
  mission?: { title?: string; goal?: string; starting_state?: string; final_state?: string };
  milestones?: Array<{ question_id: string; title: string; purpose?: string; unlocks?: string }>;
  introduction: string;
  refresher?: string | {
    concept?: string;
    explanation?: string;
    worked_example?: string | { question?: string; steps?: string[]; answer?: string };
  };
  activities: Array<{ activity_number: number; questions: LessonQuestion[] }>;
  conclusion: string;
  story_complexity?: string;
  alignment_warning?: string | null;
};

// AI-ASSISTED ADDITION: This component only simulates completion for UI testing.
// The future student player must use verified answers before recording progress.


export default function LessonRenderer({lesson,studentName,studentInterests,studentId}:{
 lesson:RenderableLesson;studentName?:string;studentInterests?:string;studentId?:string
}){
 return <TeacherLessonPlayer lesson={lesson} studentName={studentName} studentInterests={studentInterests} studentId={studentId}/>;
}
