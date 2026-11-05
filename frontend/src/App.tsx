/**
 * Purpose: Main React application, role navigation, and student data loading.
 *
 * Original application structure: Existing Sonoran Hot Data project code.
 * AI-assisted addition (2026-11-05): Temporary Fraction Fortress mock
 * lesson preview navigation and rendering.
 *
 * Directed and reviewed by: Edenna Chen
 * Code generated with assistance from: ChatGPT (OpenAI), GPT-6
 * Human edits: Existing project code preserved.
 * External sources: None.
 *
 * Notes:
 * - Preserves student and teacher interfaces and FastAPI demo student loading.
 * - Mock Lesson is a standalone preview; it does not update mastery,
 *   completion counts, pet growth, or database records.
 */

import { useEffect, useState } from 'react';

import Sidebar from './components/Sidebar';

import Home from './pages/student/Home';
import Calibration from './pages/student/Calibration';
import Learn from './pages/student/Learn';
import Profile from './pages/student/Profile';
import Avatar from './pages/student/Avatar';

import Dashboard from './pages/teacher/Dashboard';
import Students from './pages/teacher/Students';
import Assignments from './pages/teacher/Assignments';
import Analytics from './pages/teacher/Analytics';
import Settings from './pages/teacher/Settings';

import { useLocalState } from './hooks/useLocalState';

import { getDemoStudents } from './api/students';
import type { ApiStudent } from './api/students';

import { initialStudents } from './data/mock';
import type { Role, Student } from './types';

// AI-assisted: Standalone hardcoded lesson preview component.
import MockLesson from './components/lesson/MockLesson';

export default function App() {
  // Existing application navigation.
  const [role, setRole] = useState<Role | null>(null);
  const [page, setPage] = useState('Home');

  // Existing frontend demo data.
  const [students, setStudents] = useLocalState<Student[]>(
    'adaptive-demo-students',
    initialStudents
  );

  // Existing FastAPI demo student loading.
  const [demoStudents, setDemoStudents] = useState<ApiStudent[]>([]);
  const [studentsLoading, setStudentsLoading] = useState(true);
  const [studentsError, setStudentsError] = useState<string | null>(null);

  const [selectedStudentId, setSelectedStudentId] =
    useState<string | null>(null);

  useEffect(() => {
    let active = true;

    getDemoStudents()
      .then(data => {
        if (active) {
          setDemoStudents(data);
        }
      })
      .catch(error => {
        if (active) {
          setStudentsError(
            error instanceof Error
              ? error.message
              : 'Unable to load students'
          );
        }
      })
      .finally(() => {
        if (active) {
          setStudentsLoading(false);
        }
      });

    return () => {
      active = false;
    };
  }, []);

  const backendStatus = studentsLoading
    ? 'Loading students...'
    : studentsError
      ? 'Student API unavailable'
      : `${demoStudents.length} demo students loaded`;

  // Existing student portal uses the first mock student.
  const student = students[0];

  const updateStudent = (
    id: string,
    changes: Partial<Student>
  ) => {
    setStudents(prev =>
      prev.map(s =>
        s.id === id ? { ...s, ...changes } : s
      )
    );
  };

  const chooseRole = (next: Role) => {
    setRole(next);
    setPage(next === 'student' ? 'Home' : 'Dashboard');
  };

  if (!role) {
    return (
      <div className="role-entry">
        <div className="role-entry-card">
          <div className="logo-mark">✦</div>

          <p className="eyebrow">ADAPTIVE CLASSROOM</p>

          <h1>How would you like to explore?</h1>

          <p className="lead">
            Choose a view to explore the classroom prototype.
            No login needed.
          </p>

          <div className="role-cards">
            <button
              className="role-card"
              onClick={() => chooseRole('student')}
            >
              <span>🎒</span>
              <strong>Student</strong>
              <small>
                Lessons, calibration, profile and avatar
              </small>
            </button>

            <button
              className="role-card"
              onClick={() => chooseRole('teacher')}
            >
              <span>📋</span>
              <strong>Teacher</strong>
              <small>
                Class overview, students and assignments
              </small>
            </button>
          </div>

          <p className="muted small">
            Demo only — switch roles at any time.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell">
      <Sidebar
        role={role}
        page={page}
        onNavigate={setPage}
        onSignOut={() => setRole(null)}
      />

      <main className="main-content">
        <header className="topbar">
          <span>
            {role === 'student'
              ? 'Student portal'
              : 'Teacher portal'}
          </span>

          <span className="topbar-account">
            {role === 'student' ? student.avatar : '📋'}
            {' '}Demo view
          </span>
        </header>

        {/* AI-assisted: Temporary preview controls for student testing only. */}
        {role === 'student' && (
          <div style={{ padding: '12px 20px', display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            {page !== 'Mock Lesson' ? (
              <button type="button" onClick={() => setPage('Mock Lesson')}>
                Preview Fraction Fortress
              </button>
            ) : (
              <button type="button" onClick={() => setPage('Home')}>
                Back to Home
              </button>
            )}
          </div>
        )}

        {role === 'student' ? (
          <>
            {/* AI-assisted: Preview only; no student progress is saved. */}
            {page === 'Mock Lesson' && <MockLesson />}

            {page === 'Home' && (
              <Home
                student={student}
                onNavigate={setPage}
              />
            )}

            {page === 'Calibration' && (
              <Calibration
                student={student}
                onUpdate={changes =>
                  updateStudent(student.id, changes)
                }
              />
            )}

            {page === 'Learn' && (
              <Learn
                student={student}
                onComplete={() =>
                  updateStudent(student.id, {
                    mastery: Math.min(
                      100,
                      student.mastery + 10
                    ),
                    completed: student.completed + 1,
                  })
                }
              />
            )}

            {page === 'Profile' && (
              <Profile
                student={student}
                onNavigate={setPage}
              />
            )}

            {page === 'Avatar' && (
              <Avatar
                student={student}
                onUpdate={changes =>
                  updateStudent(student.id, changes)
                }
              />
            )}
          </>
        ) : (
          <>
            {/* Existing temporary backend connection indicator. */}
            <p className="muted small" role="status">
              {backendStatus}
            </p>

            {page === 'Dashboard' && (
              <Dashboard
                students={demoStudents}
                loading={studentsLoading}
                error={studentsError}
                onSelectStudent={studentId => {
                  setSelectedStudentId(studentId);
                  setPage('Students');
                }}
              />
            )}

            {page === 'Students' && (
              <Students
                students={demoStudents}
                selectedStudentId={selectedStudentId}
                onCreateLesson={studentId => {
                  setSelectedStudentId(studentId);
                  setPage('Assignments');
                }}
              />
            )}

            {page === 'Assignments' && (
              <Assignments
                students={demoStudents}
                selectedStudentId={selectedStudentId}
              />
            )}

            {page === 'Analytics' && (
              <Analytics students={students} />
            )}

            {page === 'Settings' && (
              <Settings />
            )}
          </>
        )}
      </main>
    </div>
  );
}
