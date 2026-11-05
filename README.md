# Sonoran Avatar: sharp editor + full-body lesson sprite

Install from repository root: `unzip -o ~/Downloads/Avatar_FullBody_Lesson_Update.zip -d .` then `cd frontend && npx tsc --noEmit && npm run dev`.

Changes:
- Editor uses Miguel's original SVG at native sharp resolution, cropping out pet with viewBox. No companion controls shown.
- Backend still requires and stores a pet: no backend code or student records changed.
- LessonScene replaces only the hardcoded fox with a stepped full-body SVG sprite based on editor choices, with no pet.
- MockLesson V4 passes locally previewed editor choices into LessonScene. Reopen Mock Lesson after editing. Demo preview is stored in localStorage only; not grading or persistence.
- Reduce motion checkbox remains at bottom and is styled; native checkbox is used for accessibility.
- No external assets, images, or paid API calls.

MUST TODO:
1. Restore configurable VITE_API_URL with vite/client typing and shared config.
2. Map mock student IDs to real backend UUIDs before enabling save.
3. Make pet truly optional in backend model/renderer, rather than merely hiding it in UI.
4. Connect real saved avatar choices to lesson rendering (demo currently uses localStorage).
5. Improve pixel sprite variants and movement/accessibility; preserve existing lesson artwork.
6. Connect AI lesson background generation with teacher approval.

NOTE: ZIP includes V4 MockLesson and LessonScene; back up these two files if you have newer local changes before installing. Does not change questions in V4.
