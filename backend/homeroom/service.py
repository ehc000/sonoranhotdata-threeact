
import uuid

from backend.database.connection import get_connection


def create_educator(name, email=None, subject=None, points_enabled=False):
    """Create an educator in the shared database."""
    educator_id = str(uuid.uuid4())

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO educators
                (id, name, email, subject, points_enabled)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                educator_id,
                name,
                email,
                subject,
                int(points_enabled),
            ),
        )

    return educator_id


def create_class(name, educator_id=None, capacity=25):
    """Create a class in the shared database."""
    if capacity < 1:
        raise ValueError("Class capacity must be positive")

    class_id = str(uuid.uuid4())

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO classes
                (id, name, educator_id, capacity)
            VALUES (?, ?, ?, ?)
            """,
            (class_id, name, educator_id, capacity),
        )

    return class_id


def enroll_student(student_id, class_id):
    """Enroll an existing student in a class."""

    with get_connection() as conn:
        classroom = conn.execute(
            """
            SELECT capacity
            FROM classes
            WHERE id = ?
            """,
            (class_id,),
        ).fetchone()

        if classroom is None:
            raise ValueError("Class not found")

        current_count = conn.execute(
            """
            SELECT COUNT(*)
            FROM enrollments
            WHERE class_id = ?
            """,
            (class_id,),
        ).fetchone()[0]

        if current_count >= classroom["capacity"]:
            raise ValueError("Class is full")

        conn.execute(
            """
            INSERT INTO enrollments (student_id, class_id)
            VALUES (?, ?)
            """,
            (student_id, class_id),
        )


def auto_enroll_student(student_id):
    """
    Assign a student to an available class.

    If all classes are full, create a new class.
    Each student may belong to only one class.
    """

    with get_connection() as conn:
        student = conn.execute(
            "SELECT id FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

        if student is None:
            raise ValueError("Student not found")

        # Check whether student is already enrolled.
        existing = conn.execute(
            """
            SELECT class_id
            FROM enrollments
            WHERE student_id = ?
            """,
            (student_id,),
        ).fetchone()

        if existing:
            return existing["class_id"]

        # Find a class with available capacity.
        classroom = conn.execute(
            """
            SELECT c.id
            FROM classes c
            LEFT JOIN enrollments en ON c.id = en.class_id
            GROUP BY c.id
            HAVING COUNT(en.student_id) < c.capacity
            ORDER BY COUNT(en.student_id), c.name
            LIMIT 1
            """
        ).fetchone()

        if classroom:
            class_id = classroom["id"]

        else:
            # Choose the educator with the fewest classes.
            educator = conn.execute(
                """
                SELECT e.id
                FROM educators e
                LEFT JOIN classes c ON e.id = c.educator_id
                GROUP BY e.id
                ORDER BY COUNT(c.id), e.name
                LIMIT 1
                """
            ).fetchone()

            educator_id = educator["id"] if educator else None

            class_id = str(uuid.uuid4())

            conn.execute(
                """
                INSERT INTO classes
                    (id, name, educator_id, capacity)
                VALUES (?, ?, ?, 25)
                """,
                (
                    class_id,
                    f"Homeroom {class_id[:8]}",
                    educator_id,
                ),
            )

        conn.execute(
            """
            INSERT INTO enrollments (student_id, class_id)
            VALUES (?, ?)
            """,
            (student_id, class_id),
        )

    return class_id


def create_project(class_id, title, total_steps):
    """Create a project for a classroom."""
    if not 1 <= total_steps <= 50:
        raise ValueError("Project must have 1–50 steps")

    project_id = str(uuid.uuid4())

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO projects (id, class_id, title, total_steps)
            VALUES (?, ?, ?, ?)
            """,
            (project_id, class_id, title, total_steps),
        )

    return project_id


def update_project_progress(student_id, project_id, steps_done):
    """Save a student's progress on a classroom project."""
    with get_connection() as conn:
        project = conn.execute(
            """
            SELECT class_id, total_steps
            FROM projects
            WHERE id = ?
            """,
            (project_id,),
        ).fetchone()

        if project is None:
            raise ValueError("Project not found")

        enrolled = conn.execute(
            """
            SELECT 1 FROM enrollments
            WHERE student_id = ? AND class_id = ?
            """,
            (student_id, project["class_id"]),
        ).fetchone()

        if enrolled is None:
            raise ValueError("Student is not enrolled in this class")

        if not 0 <= steps_done <= project["total_steps"]:
            raise ValueError("Invalid number of completed steps")

        conn.execute(
            """
            INSERT INTO project_progress
                (student_id, project_id, steps_done)
            VALUES (?, ?, ?)
            ON CONFLICT(student_id, project_id)
            DO UPDATE SET steps_done = excluded.steps_done
            """,
            (student_id, project_id, steps_done),
        )


def get_student_projects(student_id):
    """Retrieve all projects assigned to a student's class."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT p.id, p.title, p.total_steps,
                   COALESCE(pp.steps_done, 0) AS steps_done
            FROM projects p
            JOIN enrollments e ON e.class_id = p.class_id
            LEFT JOIN project_progress pp
                ON pp.project_id = p.id
                AND pp.student_id = e.student_id
            WHERE e.student_id = ?
            ORDER BY p.title
            """,
            (student_id,),
        ).fetchall()

    return [dict(row) for row in rows]


def get_class_progress(class_id):
    """Retrieve project progress for all enrolled students."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT s.id AS student_id, s.name AS student_name,
                   p.id AS project_id, p.title,
                   p.total_steps,
                   COALESCE(pp.steps_done, 0) AS steps_done
            FROM enrollments e
            JOIN students s ON s.id = e.student_id
            JOIN projects p ON p.class_id = e.class_id
            LEFT JOIN project_progress pp
                ON pp.student_id = s.id
                AND pp.project_id = p.id
            WHERE e.class_id = ?
            ORDER BY s.name, p.title
            """,
            (class_id,),
        ).fetchall()

    return [dict(row) for row in rows]

