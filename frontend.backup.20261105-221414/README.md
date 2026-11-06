# Playable teacher preview — TypeScript fix
From `sonoranhotdata` root:
```bash
unzip -o ~/Downloads/Teacher_Playable_Preview_TS_Fix.zip -d .
python3 scripts/fix_playable_preview.py
cd frontend
npx tsc --noEmit
```
Fixes the syntax error at LessonRenderer.tsx line 45 introduced by the earlier installer and removes an unused type import. No lesson content is changed.

If TypeScript reports additional errors, share the new output. This patch has not been compiled against your complete local repository.
