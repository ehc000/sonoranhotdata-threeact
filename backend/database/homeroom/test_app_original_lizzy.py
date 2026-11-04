"""Homeroom: student and educator profiles with a class point system.
Run in a terminal:  python homeroom.py
"""
import os
import re
import sqlite3

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "school.db")
CLASS_CAPACITY = 25   # students per class; a new class opens when one is full
WELCOME_POINTS = 10   # bonus for students in a class whose educator has points ON
WELCOME_REASON = "Welcome bonus"
MAX_AWARD = 1000      # largest single award/deduction an educator can make
MIN_GRADE, MAX_GRADE = 0, 12   # 0 = kindergarten
MAX_STEPS = 50        # most steps (milestones) a single project can have


# ---------- input validation ----------

def clean_email(email):
    """Trim and lowercase so 'Ann@X.com' and 'ann@x.com' are the same person."""
    email = (email or "").strip().lower()
    if len(email) > 254 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValueError("Please enter a valid email address")
    return email


def clean_text(value, label, max_len=100):
    value = (value or "").strip()
    if not value:
        raise ValueError(f"{label} must not be blank")
    if len(value) > max_len:
        raise ValueError(f"{label} must be at most {max_len} characters")
    return value


def clean_grade(value):
    try:
        grade = int(str(value).strip())
    except ValueError:
        raise ValueError("Grade level must be a whole number")
    if not MIN_GRADE <= grade <= MAX_GRADE:
        raise ValueError(f"Grade level must be between {MIN_GRADE} and {MAX_GRADE}")
    return grade


def get_connection(path=None):
    conn = sqlite3.connect(path or DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS students (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT NOT NULL,
        email       TEXT NOT NULL UNIQUE,
        grade_level INTEGER,
        points      INTEGER NOT NULL DEFAULT 0 CHECK (points >= 0),
        created_at  TEXT DEFAULT CURRENT_TIMESTAMP
    );

    -- Educators have a points *setting*, but no points balance of their own
    CREATE TABLE IF NOT EXISTS educators (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        name           TEXT NOT NULL,
        email          TEXT NOT NULL UNIQUE,
        subject        TEXT,
        points_enabled INTEGER NOT NULL DEFAULT 0 CHECK (points_enabled IN (0, 1)),
        created_at     TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS classes (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT NOT NULL,
        capacity    INTEGER NOT NULL,
        educator_id INTEGER REFERENCES educators(id),
        created_at  TEXT DEFAULT CURRENT_TIMESTAMP
    );

    -- A student belongs to exactly one class (UNIQUE on student_id)
    CREATE TABLE IF NOT EXISTS enrollments (
        student_id  INTEGER NOT NULL UNIQUE REFERENCES students(id),
        class_id    INTEGER NOT NULL REFERENCES classes(id)
    );

    -- Ledger: every point change, who gave it, and why
    CREATE TABLE IF NOT EXISTS point_transactions (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id  INTEGER NOT NULL REFERENCES students(id),
        educator_id INTEGER REFERENCES educators(id),  -- NULL = system (welcome bonus)
        amount      INTEGER NOT NULL CHECK (amount != 0),
        reason      TEXT NOT NULL,
        created_at  TEXT DEFAULT CURRENT_TIMESTAMP
    );

    -- Projects belong to a class; every student in that class works on them
    CREATE TABLE IF NOT EXISTS projects (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id    INTEGER NOT NULL REFERENCES classes(id),
        title       TEXT NOT NULL,
        total_steps INTEGER NOT NULL CHECK (total_steps BETWEEN 1 AND 50),
        created_at  TEXT DEFAULT CURRENT_TIMESTAMP
    );

    -- How far each student is on each project (no row yet = 0 steps done)
    CREATE TABLE IF NOT EXISTS project_progress (
        student_id  INTEGER NOT NULL REFERENCES students(id),
        project_id  INTEGER NOT NULL REFERENCES projects(id),
        steps_done  INTEGER NOT NULL DEFAULT 0 CHECK (steps_done >= 0),
        updated_at  TEXT DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (student_id, project_id)
    );
    """)
    # Migrations for databases created by earlier versions
    student_cols = [r["name"] for r in conn.execute("PRAGMA table_info(students)")]
    if "points" not in student_cols:
        conn.execute("ALTER TABLE students ADD COLUMN points INTEGER NOT NULL DEFAULT 0")
    educator_cols = [r["name"] for r in conn.execute("PRAGMA table_info(educators)")]
    if "points_enabled" not in educator_cols:
        conn.execute("ALTER TABLE educators ADD COLUMN points_enabled INTEGER NOT NULL DEFAULT 0")
    conn.commit()


# ---------- class helpers ----------

def least_busy_educator(conn):
    """Educator with the fewest classes, or None if there are no educators."""
    row = conn.execute("""
        SELECT e.id
        FROM educators e
        LEFT JOIN classes c ON c.educator_id = e.id
        GROUP BY e.id
        ORDER BY COUNT(c.id), e.id
        LIMIT 1
    """).fetchone()
    return row["id"] if row else None


def open_class_id(conn):
    """First class that still has room, or None."""
    row = conn.execute("""
        SELECT c.id
        FROM classes c
        LEFT JOIN enrollments en ON en.class_id = c.id
        GROUP BY c.id
        HAVING COUNT(en.student_id) < c.capacity
        ORDER BY c.id
        LIMIT 1
    """).fetchone()
    return row["id"] if row else None


def create_class(conn):
    number = conn.execute("SELECT COUNT(*) FROM classes").fetchone()[0] + 1
    cur = conn.execute(
        "INSERT INTO classes (name, capacity, educator_id) VALUES (?, ?, ?)",
        (f"Class {number}", CLASS_CAPACITY, least_busy_educator(conn)),
    )
    return cur.lastrowid


# ---------- point system settings ----------

def points_active_for_class(conn, class_id):
    """True if the class has an educator whose point system is ON."""
    row = conn.execute("""
        SELECT e.points_enabled FROM classes c
        JOIN educators e ON e.id = c.educator_id
        WHERE c.id = ?
    """, (class_id,)).fetchone()
    return bool(row and row["points_enabled"])


def grant_welcome_bonuses(conn, educator_id):
    """Give the welcome bonus to this educator's students who haven't had it yet.
    Call inside a transaction. Returns how many students received it."""
    rows = conn.execute("""
        SELECT s.id FROM students s
        JOIN enrollments en ON en.student_id = s.id
        JOIN classes c ON c.id = en.class_id
        WHERE c.educator_id = ?
          AND NOT EXISTS (SELECT 1 FROM point_transactions t
                          WHERE t.student_id = s.id AND t.reason = ?
                            AND t.educator_id IS NULL)
    """, (educator_id, WELCOME_REASON)).fetchall()
    if WELCOME_POINTS:
        for r in rows:
            _apply_points(conn, r["id"], WELCOME_POINTS, WELCOME_REASON)
    return len(rows) if WELCOME_POINTS else 0


def set_points_enabled(conn, educator_email, enabled):
    """An educator turns the point system ON or OFF for their classes.
    Returns the number of students who received a welcome bonus."""
    educator_email = clean_email(educator_email)
    row = conn.execute("SELECT id FROM educators WHERE email = ?", (educator_email,)).fetchone()
    if row is None:
        raise ValueError("No educator with that email")
    with conn:
        conn.execute("UPDATE educators SET points_enabled = ? WHERE id = ?",
                     (1 if enabled else 0, row["id"]))
        return grant_welcome_bonuses(conn, row["id"]) if enabled else 0


# ---------- points ----------

def _apply_points(conn, student_id, amount, reason, educator_id=None):
    """Update the running total and write the ledger row. Call inside a transaction."""
    row = conn.execute("SELECT points FROM students WHERE id = ?", (student_id,)).fetchone()
    if row is None:
        raise ValueError("Student not found")
    if row["points"] + amount < 0:
        raise ValueError(f"Cannot deduct {-amount}: student only has {row['points']} points")
    conn.execute("UPDATE students SET points = points + ? WHERE id = ?", (amount, student_id))
    conn.execute(
        "INSERT INTO point_transactions (student_id, educator_id, amount, reason) "
        "VALUES (?, ?, ?, ?)",
        (student_id, educator_id, amount, reason),
    )


def award_points(conn, educator_email, student_email, amount, reason):
    """An educator awards (positive) or deducts (negative) points for a student in
    one of their classes. Only allowed while the educator's point system is ON."""
    if not isinstance(amount, int) or isinstance(amount, bool):
        raise ValueError("Points must be a whole number")
    if amount == 0:
        raise ValueError("Amount must not be zero")
    if abs(amount) > MAX_AWARD:
        raise ValueError(f"You can award or deduct at most {MAX_AWARD} points at a time")
    reason = clean_text(reason, "Reason", max_len=200)
    educator_email = clean_email(educator_email)
    student_email = clean_email(student_email)

    educator = conn.execute(
        "SELECT id, points_enabled FROM educators WHERE email = ?",
        (educator_email,)).fetchone()
    if educator is None:
        raise ValueError("No educator with that email")
    if not educator["points_enabled"]:
        raise ValueError("Your point system is OFF. Turn it on first")

    student = conn.execute("""
        SELECT s.id FROM students s
        JOIN enrollments en ON en.student_id = s.id
        JOIN classes c ON c.id = en.class_id
        WHERE s.email = ? AND c.educator_id = ?
    """, (student_email, educator["id"])).fetchone()
    if student is None:
        raise ValueError("That student is not in one of your classes")

    with conn:
        _apply_points(conn, student["id"], amount, reason, educator["id"])
    return conn.execute(
        "SELECT points FROM students WHERE id = ?", (student["id"],)).fetchone()["points"]


def point_history(conn, student_email):
    return conn.execute("""
        SELECT t.amount, t.reason, t.created_at, e.name AS given_by
        FROM point_transactions t
        JOIN students s ON s.id = t.student_id
        LEFT JOIN educators e ON e.id = t.educator_id
        WHERE s.email = ?
        ORDER BY t.id DESC
    """, (clean_email(student_email),)).fetchall()


def leaderboard(conn, class_id=None, limit=10):
    """Only students in classes whose educator has the point system ON."""
    sql = """
        SELECT s.name, s.points, c.name AS class_name
        FROM students s
        JOIN enrollments en ON en.student_id = s.id
        JOIN classes c ON c.id = en.class_id
        JOIN educators e ON e.id = c.educator_id
        WHERE e.points_enabled = 1
    """
    params = []
    if class_id is not None:
        sql += " AND c.id = ?"
        params.append(class_id)
    sql += " ORDER BY s.points DESC, s.name LIMIT ?"
    params.append(limit)
    return conn.execute(sql, params).fetchall()


# ---------- projects & progress ----------

def progress_bar(done, total, width=20):
    """Text progress bar, e.g. [########------------] 40%"""
    total = max(total, 1)
    filled = round(width * done / total)
    return f"[{'#' * filled}{'-' * (width - filled)}] {100 * done // total}%"


def educator_classes(conn, educator_email):
    return conn.execute("""
        SELECT c.id, c.name FROM classes c JOIN educators e ON e.id = c.educator_id
        WHERE e.email = ? ORDER BY c.id""", (clean_email(educator_email),)).fetchall()


def create_project(conn, educator_email, class_id, title, total_steps):
    """An educator adds a project to one of their classes. Every student in the
    class (now or later) starts at 0 of total_steps."""
    title = clean_text(title, "Project title")
    if not isinstance(total_steps, int) or isinstance(total_steps, bool) \
            or not 1 <= total_steps <= MAX_STEPS:
        raise ValueError(f"Steps must be a whole number from 1 to {MAX_STEPS}")
    owns = conn.execute("""
        SELECT 1 FROM classes c JOIN educators e ON e.id = c.educator_id
        WHERE c.id = ? AND e.email = ?""", (class_id, clean_email(educator_email))).fetchone()
    if owns is None:
        raise ValueError("That is not one of your classes")
    with conn:
        cur = conn.execute("INSERT INTO projects (class_id, title, total_steps) VALUES (?, ?, ?)",
                           (class_id, title, total_steps))
    return cur.lastrowid


def student_projects(conn, student_email):
    """Every project in the student's class with how many steps they have finished."""
    return conn.execute("""
        SELECT p.id, p.title, p.total_steps, COALESCE(pp.steps_done, 0) AS steps_done
        FROM students s
        JOIN enrollments en ON en.student_id = s.id
        JOIN projects p ON p.class_id = en.class_id
        LEFT JOIN project_progress pp ON pp.student_id = s.id AND pp.project_id = p.id
        WHERE s.email = ? ORDER BY p.id""", (clean_email(student_email),)).fetchall()


def overall_progress(projects):
    """(steps done, total steps) across a list of student_projects rows."""
    return (sum(p["steps_done"] for p in projects), sum(p["total_steps"] for p in projects))


def update_progress(conn, student_email, project_id, steps_done):
    """A student sets how many steps of a project they have finished."""
    if not isinstance(steps_done, int) or isinstance(steps_done, bool):
        raise ValueError("Steps done must be a whole number")
    row = conn.execute("""
        SELECT s.id AS student_id, p.total_steps
        FROM students s
        JOIN enrollments en ON en.student_id = s.id
        JOIN projects p ON p.class_id = en.class_id
        WHERE s.email = ? AND p.id = ?""", (clean_email(student_email), project_id)).fetchone()
    if row is None:
        raise ValueError("That project is not in your class")
    if not 0 <= steps_done <= row["total_steps"]:
        raise ValueError(f"Steps done must be between 0 and {row['total_steps']}")
    with conn:
        conn.execute("""
            INSERT INTO project_progress (student_id, project_id, steps_done) VALUES (?, ?, ?)
            ON CONFLICT (student_id, project_id)
            DO UPDATE SET steps_done = excluded.steps_done, updated_at = CURRENT_TIMESTAMP
        """, (row["student_id"], project_id, steps_done))


def educator_progress(conn, educator_email):
    """Per-project, per-student progress for all of an educator's classes."""
    return conn.execute("""
        SELECT p.id AS project_id, p.title, p.total_steps, c.name AS class_name,
               s.name AS student, COALESCE(pp.steps_done, 0) AS steps_done
        FROM projects p
        JOIN classes c ON c.id = p.class_id
        JOIN educators e ON e.id = c.educator_id
        LEFT JOIN enrollments en ON en.class_id = c.id
        LEFT JOIN students s ON s.id = en.student_id
        LEFT JOIN project_progress pp ON pp.project_id = p.id AND pp.student_id = s.id
        WHERE e.email = ? ORDER BY p.id, s.name""", (clean_email(educator_email),)).fetchall()


# ---------- profile creation ----------

def create_student(conn, name, email, grade_level):
    """Store the student and place them in a class (opening a new one if needed).
    They get the welcome bonus only if that class's educator has points ON."""
    name = clean_text(name, "Name")
    email = clean_email(email)
    grade_level = clean_grade(grade_level)
    with conn:  # one transaction: all-or-nothing
        cur = conn.execute(
            "INSERT INTO students (name, email, grade_level) VALUES (?, ?, ?)",
            (name, email, grade_level),
        )
        student_id = cur.lastrowid
        class_id = open_class_id(conn) or create_class(conn)
        conn.execute(
            "INSERT INTO enrollments (student_id, class_id) VALUES (?, ?)",
            (student_id, class_id),
        )
        if WELCOME_POINTS and points_active_for_class(conn, class_id):
            _apply_points(conn, student_id, WELCOME_POINTS, WELCOME_REASON)
    return student_id, class_id


def create_educator(conn, name, email, subject, points_enabled=False):
    """Store the educator (choosing whether to use the point system), then give them
    any classes that have no teacher yet."""
    name = clean_text(name, "Name")
    email = clean_email(email)
    subject = clean_text(subject, "Subject")
    with conn:
        cur = conn.execute(
            "INSERT INTO educators (name, email, subject, points_enabled) VALUES (?, ?, ?, ?)",
            (name, email, subject, 1 if points_enabled else 0),
        )
        educator_id = cur.lastrowid
        conn.execute(
            "UPDATE classes SET educator_id = ? WHERE educator_id IS NULL",
            (educator_id,),
        )
        if points_enabled:
            grant_welcome_bonuses(conn, educator_id)
    return educator_id


def create_profile(conn, role, name, email, extra, points_enabled=False):
    try:
        if role == "student":
            return create_student(conn, name, email, extra)
        if role == "educator":
            return create_educator(conn, name, email, extra, points_enabled)
        raise ValueError("role must be 'student' or 'educator'")
    except sqlite3.IntegrityError as err:
        if "UNIQUE" in str(err):
            raise ValueError(f"That email is already registered as a {role}")
        raise


# ---------- terminal app ----------

def rule():
    print("-" * 46)


def yes_no(prompt):
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please type y or n.")


def ask_int(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        raise ValueError("Please enter a whole number")


def find_user(conn, email):
    """Return ('student' | 'educator', email) for a registered email."""
    email = clean_email(email)
    for role, table in (("student", "students"), ("educator", "educators")):
        if conn.execute(f"SELECT 1 FROM {table} WHERE email = ?", (email,)).fetchone():
            return role, email
    raise ValueError("No account with that email. Choose 'Create account' first.")


def pick(options):
    """Show a numbered menu, return the chosen number as a string."""
    print()
    for i, text in enumerate(options, 1):
        print(f"  {i}) {text}")
    return input("> ").strip()


# ----- student -----

def student_summary(conn, email):
    return conn.execute("""
        SELECT s.name, s.grade_level, s.points, c.id AS class_id, c.name AS class_name,
               e.name AS educator, COALESCE(e.points_enabled, 0) AS points_on
        FROM students s
        LEFT JOIN enrollments en ON en.student_id = s.id
        LEFT JOIN classes c ON c.id = en.class_id
        LEFT JOIN educators e ON e.id = c.educator_id
        WHERE s.email = ?""", (email,)).fetchone()


def show_projects(projects):
    if not projects:
        print("No projects yet. Your teacher will add them.")
    for p in projects:
        print(f"  {p['title']}")
        print(f"    {progress_bar(p['steps_done'], p['total_steps'])}  "
              f"{p['steps_done']}/{p['total_steps']} steps")


def student_home(conn, email):
    while True:
        s = student_summary(conn, email)
        projects = student_projects(conn, email)
        print()
        rule()
        print(f" {s['name']}  |  Grade {s['grade_level']}  |  {s['class_name']}")
        print(f" Teacher: {s['educator'] or 'not assigned yet'}")
        print(f" Points: {s['points']}" if s["points_on"]
              else " Your teacher hasn't turned on points yet.")
        if projects:
            print(f" All projects: {progress_bar(*overall_progress(projects))}")
        rule()
        choice = pick(["My projects", "Update my project progress",
                       "My point history", "Class leaderboard", "Sign out"])
        try:
            if choice == "1":
                print()
                show_projects(projects)
            elif choice == "2":
                if not projects:
                    raise ValueError("There are no projects in your class yet")
                print()
                for i, p in enumerate(projects, 1):
                    print(f"  {i}) {p['title']}  ({p['steps_done']}/{p['total_steps']} steps)")
                n = ask_int("Which project? ")
                if not 1 <= n <= len(projects):
                    raise ValueError("Please pick a number from the list")
                p = projects[n - 1]
                done = ask_int(f"Steps you have finished (0-{p['total_steps']}): ")
                update_progress(conn, email, p["id"], done)
                print(f"Saved. {p['title']}: {progress_bar(done, p['total_steps'])}")
            elif choice == "3":
                if not s["points_on"]:
                    raise ValueError("Points aren't turned on for your class")
                history = point_history(conn, email)
                if not history:
                    print("No points yet.")
                for t in history:
                    print(f"  {t['amount']:+d}  {t['reason']}  "
                          f"({t['given_by'] or 'System'}, {t['created_at'][:10]})")
            elif choice == "4":
                rows = leaderboard(conn, s["class_id"]) if s["points_on"] else []
                if not rows:
                    raise ValueError("No leaderboard: points aren't turned on for your class")
                for rank, r in enumerate(rows, 1):
                    you = "  <- you" if r["name"] == s["name"] else ""
                    print(f"  {rank}. {r['name']:<20} {r['points']:>5} pts{you}")
            elif choice == "5":
                return
            else:
                print("Please choose a number from 1 to 5.")
        except ValueError as err:
            print(f"Error: {err}")


# ----- educator -----

def educator_students(conn, email):
    return conn.execute("""
        SELECT s.name, s.email, s.points, s.grade_level, c.name AS class_name
        FROM students s
        JOIN enrollments en ON en.student_id = s.id
        JOIN classes c ON c.id = en.class_id
        JOIN educators e ON e.id = c.educator_id
        WHERE e.email = ? ORDER BY c.id, s.name""", (email,)).fetchall()


def educator_home(conn, email):
    while True:
        e = conn.execute("SELECT name, subject, points_enabled FROM educators WHERE email = ?",
                         (email,)).fetchone()
        on = bool(e["points_enabled"])
        print()
        rule()
        print(f" {e['name']}  |  {e['subject']}  |  Point system: {'ON' if on else 'OFF'}")
        rule()
        choice = pick(["My classes and students", "Award / deduct points",
                       "Create a project", "Project progress",
                       f"Turn point system {'OFF' if on else 'ON'}", "Sign out"])
        try:
            if choice == "1":
                students = educator_students(conn, email)
                if not students:
                    print("No students yet. Classes open as students sign up.")
                last = None
                for s in students:
                    if s["class_name"] != last:
                        last = s["class_name"]
                        print(f"\n  {last}")
                    pts = f"  [{s['points']} pts]" if on else ""
                    print(f"    - {s['name']} (grade {s['grade_level']}, {s['email']}){pts}")
            elif choice == "2":
                if not on:
                    raise ValueError("Your point system is OFF. Turn it on first.")
                students = educator_students(conn, email)
                if not students:
                    raise ValueError("You have no students yet")
                print()
                for i, s in enumerate(students, 1):
                    print(f"  {i}) {s['name']}  ({s['class_name']}, {s['points']} pts)")
                n = ask_int("Which student? ")
                if not 1 <= n <= len(students):
                    raise ValueError("Please pick a number from the list")
                amount = ask_int("Points (negative to deduct): ")
                reason = input("Reason: ")
                total = award_points(conn, email, students[n - 1]["email"], amount, reason)
                print(f"Done. {students[n - 1]['name']} now has {total} points.")
            elif choice == "3":
                classes = educator_classes(conn, email)
                if not classes:
                    raise ValueError("You have no classes yet. They open as students sign up.")
                print()
                for i, c in enumerate(classes, 1):
                    print(f"  {i}) {c['name']}")
                n = ask_int("Which class? ")
                if not 1 <= n <= len(classes):
                    raise ValueError("Please pick a number from the list")
                title = input("Project title: ")
                steps = ask_int(f"Number of steps to finish it (1-{MAX_STEPS}): ")
                create_project(conn, email, classes[n - 1]["id"], title, steps)
                print(f"Project added to {classes[n - 1]['name']}. Students start at 0%.")
            elif choice == "4":
                rows = educator_progress(conn, email)
                if not rows:
                    print("No projects yet. Create one first.")
                last = None
                for r in rows:
                    if r["project_id"] != last:
                        last = r["project_id"]
                        print(f"\n  {r['title']}  ({r['class_name']}, {r['total_steps']} steps)")
                    if r["student"] is None:
                        print("    No students in this class yet.")
                    else:
                        print(f"    {r['student']:<20} "
                              f"{progress_bar(r['steps_done'], r['total_steps'])}")
            elif choice == "5":
                granted = set_points_enabled(conn, email, not on)
                print(f"Point system is now {'OFF' if on else 'ON'}.")
                if granted:
                    print(f"{granted} student(s) received the welcome bonus.")
            elif choice == "6":
                return
            else:
                print("Please choose a number from 1 to 6.")
        except ValueError as err:
            print(f"Error: {err}")


# ----- start screen -----

def enter(conn, role, email):
    (student_home if role == "student" else educator_home)(conn, email)
    print("Signed out.")


def create_account(conn):
    print("\nI am a...")
    who = pick(["Student", "Educator"])
    if who not in ("1", "2"):
        raise ValueError("Please choose 1 or 2")
    name = input("Full name: ")
    email = input("Email: ")
    if who == "1":
        grade = input(f"Grade level ({MIN_GRADE}-{MAX_GRADE}, 0 = kindergarten): ")
        _, class_id = create_profile(conn, "student", name, email, grade)
        print(f"\nWelcome {name.strip()}! You were placed in class #{class_id}.")
        role = "student"
    else:
        subject = input("Subject you teach: ")
        use_points = yes_no("Use a point system in your classes?")
        create_profile(conn, "educator", name, email, subject, use_points)
        print(f"\nWelcome {name.strip()}! Classes will appear as students sign up.")
        role = "educator"
    enter(conn, role, clean_email(email))


def main():
    conn = get_connection()
    init_db(conn)
    try:
        while True:
            choice = pick(["Sign in", "Create account", "Quit"])
            try:
                if choice == "1":
                    role, email = find_user(conn, input("Your email: "))
                    enter(conn, role, email)
                elif choice == "2":
                    create_account(conn)
                elif choice == "3":
                    break
                else:
                    print("Please choose a number from 1 to 3.")
            except ValueError as err:
                print(f"Error: {err}")
        print("Goodbye!")
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
    finally:
        conn.close()


if __name__ == "__main__":
    main()