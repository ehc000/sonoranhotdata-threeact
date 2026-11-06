AZACS Teacher Dashboard patch

Files replaced:
- frontend/src/App.tsx
- frontend/src/components/Sidebar.tsx
- frontend/src/pages/teacher/Dashboard.tsx
- frontend/src/pages/teacher/Analytics.tsx

Existing Students.tsx is intentionally reused without modification to preserve tile interactions, profile API calls, and teacher note saving.
The Design Lesson sidebar label continues to route internally to Assignments, preserving the lesson generator.
Analytics percentages are explicitly fictional.

Install from repository root:
  cp -R frontend "frontend.backup.$(date +%Y%m%d-%H%M%S)"
  unzip -o ~/Downloads/AZACS_Teacher_Dashboard_Final_Patch.zip
  cd frontend && npm run build
