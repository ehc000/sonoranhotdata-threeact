# Adaptive Classroom — React frontend prototype

A working **React + TypeScript + Vite** frontend for an adaptive classroom application.

## Run it

Requires a current supported Node.js LTS version (Node 20.19+ or 22.12+ recommended for Vite 6 compatibility).

```bash
npm install
npm run dev
```

Open the URL shown in Terminal (normally http://localhost:5173).

To check production compilation:

```bash
npm run build
```

## What works

- Student / Teacher choice screen (no login, passwords, or accounts)
- Separate role-specific navigation and pages
- Student: Home, Calibration, Learn, Profile, Avatar
- Teacher: Dashboard, Students, Assignments, Analytics, Settings
- Calibration preferences, avatar choices, and teacher edits
- Step-by-step fractions lesson with answer feedback and demo progress update
- Mock assignments and progress metrics
- Browser-local persistence for student data and assignments
- Responsive layout and central CSS styling in `src/styles/global.css`

## Important limitations

**This is a frontend-only demo.** There is no login or authentication. Anyone can choose either role. It is NOT safe for real student records, actual teacher permissions, or production deployment. All students and metrics are fictional sample data. `localStorage` is browser-local and not secure storage for student information.

Before real classroom use, implement authenticated accounts, backend authorization for every request, teacher-student assignment checks, secure storage, and applicable student privacy requirements. Do not enter actual student data into this demo.

## Where to customize the look

- `src/styles/global.css`: colors, typography, spacing, responsive behavior
- `src/components/Sidebar.tsx`: navigation appearance
- `src/pages/student/`: student pages
- `src/pages/teacher/`: teacher pages
- `src/App.tsx`: role selection layout

## Connecting Python and LLM APIs later

Keep Python `avatar/`, `content/`, `learning/`, `profiles/`, and `llm/` modules outside this frontend project. When ready, expose them via a server-side API (for example FastAPI) and call it from React using `fetch`. **Never put LLM API secrets in browser code or `VITE_` environment variables.**

## Testing notes

Choose Student or Teacher on the opening screen. Test calibration changes, avatar changes, the lesson, and teacher assignments. Refresh to see that sample profile data persists locally. Use Switch view in the sidebar to choose the other role. Use your browser's developer tools to test Chromebook-sized viewports.
