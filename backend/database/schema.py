from backend.database.connection import get_connection


def init_db():
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            grade_level INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS educators (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            subject TEXT,
            points_enabled INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS classes (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            educator_id TEXT REFERENCES educators(id),
            capacity INTEGER NOT NULL DEFAULT 25
        );

        CREATE TABLE IF NOT EXISTS enrollments (
            student_id TEXT NOT NULL REFERENCES students(id),
            class_id TEXT NOT NULL REFERENCES classes(id),
            PRIMARY KEY (student_id, class_id)
        );

        CREATE TABLE IF NOT EXISTS student_preferences (
            student_id TEXT PRIMARY KEY REFERENCES students(id),
            interests TEXT NOT NULL DEFAULT '[]',
            interests_text TEXT NOT NULL DEFAULT '',
            learning_preferences_text TEXT NOT NULL DEFAULT '',
            content_format TEXT NOT NULL DEFAULT 'mixed',
            sensory_sensitive INTEGER NOT NULL DEFAULT 0,
            help_mode TEXT NOT NULL DEFAULT 'offer',
            break_minutes INTEGER NOT NULL DEFAULT 2
        );

        CREATE TABLE IF NOT EXISTS student_avatars (
            student_id TEXT PRIMARY KEY REFERENCES students(id),
            avatar_json TEXT NOT NULL DEFAULT '{}',
            pet_json TEXT NOT NULL DEFAULT '{}'
        );

        CREATE TABLE IF NOT EXISTS profile_sections (
            student_id TEXT NOT NULL REFERENCES students(id),
            section TEXT NOT NULL,
            ai_summary TEXT NOT NULL DEFAULT '',
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (student_id, section)
        );

        CREATE TABLE IF NOT EXISTS teacher_notes (
            id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL REFERENCES students(id),
            section TEXT NOT NULL,
            educator_id TEXT REFERENCES educators(id),
            note_text TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS competency_progress (
            student_id TEXT NOT NULL REFERENCES students(id),
            competency TEXT NOT NULL,
            mastery_score REAL NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'not_started',
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (student_id, competency)
        );

        CREATE TABLE IF NOT EXISTS assessment_sessions (
            id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL REFERENCES students(id),
            status TEXT NOT NULL DEFAULT 'in_progress',
            session_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            class_id TEXT NOT NULL REFERENCES classes(id),
            title TEXT NOT NULL,
            total_steps INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS project_progress (
            student_id TEXT NOT NULL REFERENCES students(id),
            project_id TEXT NOT NULL REFERENCES projects(id),
            steps_done INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (student_id, project_id)
        );

        CREATE TABLE IF NOT EXISTS point_transactions (
            id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL REFERENCES students(id),
            educator_id TEXT REFERENCES educators(id),
            amount INTEGER NOT NULL,
            reason TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS pet_events (
            id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL REFERENCES students(id),
            event_type TEXT NOT NULL,
            event_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE UNIQUE INDEX IF NOT EXISTS
        dx_enrollments_one_class_per_student
        ON enrollments(student_id);
        
        """)