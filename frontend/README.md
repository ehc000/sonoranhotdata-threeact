# Teacher illustrated lesson preview (2-minute test)

Adds a visible, automatically selected SVG scene to the teacher-generated lesson preview. Uses assembled lesson content to choose space, nature, or math/adventure art. Works offline, without API keys.

**This is NOT actual AI image generation.** To render novel images from teacher visual prompts, an image-generation provider/backend endpoint must be integrated later.

Preserves student profiles, teacher approvals, academic questions, grading state, and Fraction Fortress demo. Backs up the existing LessonRenderer.tsx before editing.

From repo root:

    unzip -o ~/Downloads/Teacher_Illustrated_Preview_Quick.zip -d .
    python3 scripts/apply_visual_preview.py
    cd frontend
    npx tsc --noEmit

Then refresh your existing Vite page, open Teacher → Create a lesson, and assemble/preview a lesson. No need to restart Vite.
