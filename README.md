# Illustrated before/after lesson scenes

Install from `sonoranhotdata` root:
```bash
unzip -o ~/Downloads/Illustrated_Before_After_Lesson.zip -d .
python3 scripts/install_scene_pairs.py
cd frontend && npx tsc --noEmit
```
Restart FastAPI. Uses existing working image model via `SCENE_IMAGE_MODEL` (defaults to gpt-image-1). The before image uses the fixed style reference, and the after image uses the **actual generated before image** as its edit reference. Crossfade, slight zoom and sparkles are frontend-only. Avatar is baked into the generated before/after image; the old sliding avatar is hidden when artwork is available, but remains for fallback. Respects reduced-motion preference for transitions.

Limitations: This does **not** reuse a master *generated* scene or saved student avatar as an actual image reference across questions: every question's before frame starts from the style reference. Thus continuity across separate questions is prompt-guided, while within each before/after pair it is image-guided. The generated character may not match the saved student avatar. This is a visual prototype, not a fully verified production pipeline. Images are cached only in memory, and generated artwork is not persisted for teacher approval. Teacher-approved question text is unchanged. No grading.
