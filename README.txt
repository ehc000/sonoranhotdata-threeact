AZACS student-side quick polish
- Learn.tsx: slightly brighter island colors, labels anchored to map checkpoints, removes embedded example practice lesson.
- Avatar.tsx: design and in-lesson sprite side by side with concise headings.
- Profile.tsx: clearer mock-data notice and existing pixel avatar.
Only these three frontend pages are changed. Backend and teacher lessons are untouched.

Install from project root after backing up:
unzip -o ~/Downloads/AZACS_Student_Tiny_Polish.zip
cd frontend && npm run build

Note: The supplied Avatar.tsx did not contain a separate Fraction Fortress example button or Teacher lesson navigation button; this patch does not invent those routes. If those buttons are present in your current local file, please share that file before applying the patch to avoid overwriting them.
