Miguel avatar UI refresh — 2026-11-05

From repository root, back up then install:
  mkdir -p /tmp/sonoran-avatar-ui-backup
  cp frontend/src/components/MiguelAvatar.tsx frontend/src/pages/student/Avatar.tsx /tmp/sonoran-avatar-ui-backup/
  unzip -o ~/Downloads/Miguel_Avatar_UI_Refresh.zip -d .
  cd frontend && npx tsc --noEmit && npm run dev

Changes: compact responsive editor, avatar name first, visual color swatches, motion control last, larger sharper nearest-neighbor canvas preview. Optional hide-companion switch affects PREVIEW ONLY; Miguel's current backend requires a pet and cannot persist no companion. No changes to backend or Fraction Fortress.

MUST TODO:
1. Restore VITE_API_URL with vite/client TypeScript declarations and shared API configuration.
2. Connect frontend student IDs to backend UUIDs; saving remains disabled for s1.
3. Agree with Miguel on persistent optional companion visibility; do not silently change his schema.
4. Integrate chosen character into Moderate Fraction Fortress, keeping original scenery.
5. Refine original SVG shapes into true sprite-style art if the improved raster preview still feels soft.
