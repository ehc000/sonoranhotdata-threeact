
/**
 * File: LessonRenderer.tsx
 * Purpose: Render the same lesson for teacher preview and student playback.
 *
 * AI-assisted implementation: ChatGPT (OpenAI), GPT-6
 * Directed by: Edenna Chen
 *
 * Reference:
 * React component props:
 * https://react.dev/learn/passing-props-to-a-component
 *
 * Notes:
 * - Accepts pre-generated lesson artwork.
 * - Does not generate images during playback.
 * - Does not grade, assign, or save student progress.
 */

import TeacherLessonPlayer from './TeacherLessonPlayer';

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
  story: {
    title: string;
    story_goal?: string;
  };
  mission?: {
    title?: string;
    goal?: string;
    starting_state?: string;
    final_state?: string;
  };
  milestones?: Array<{
    question_id: string;
    title: string;
    purpose?: string;
    unlocks?: string;
  }>;
  introduction: string;
  refresher?: string | {
    concept?: string;
    explanation?: string;
    worked_example?: string | {
      question?: string;
      steps?: string[];
      answer?: string;
    };
  };
  activities: Array<{
    activity_number: number;
    questions: LessonQuestion[];
  }>;
  conclusion: string;
  story_complexity?: string;
  alignment_warning?: string | null;
};

/**
 * The format returned by POST /api/lesson-sequences/prepare.
 *
 * Images are generated and saved by the backend.
 * Animation metadata describes frontend effects.
 */
export type PreparedLessonSequence = {
  lesson_id: string;
  fingerprint: string;
  scenes: Array<{
    index: number;
    description: string;
    image_url: string;
    animation: {
      action: string;
      effect: string;
      duration_ms: number;
    };
  }>;
};

type Props = {
  lesson: RenderableLesson;
  studentName?: string;
  studentInterests?: string;
  studentId?: string;
  preparedSequence?: PreparedLessonSequence | null;
};

export default function LessonRenderer({
  lesson,
  studentName,
  studentInterests,
  studentId,
  preparedSequence,
}: Props) {
  return (
    <TeacherLessonPlayer
      lesson={lesson}
      studentName={studentName}
      studentInterests={studentInterests}
      studentId={studentId}
      preparedSequence={preparedSequence}
    />
  );
}
