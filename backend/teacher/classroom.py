
import streamlit as st

# Temporary student data
STUDENTS = [
    {
        "id": "alex",
        "name": "Alex Morgan",
        "initials": "AM",
        "project": "Build a Simple Circuit",
        "progress": 65,
        "step": "Connecting components",
        "status": "On track",
        "needs_help": False,
    },
    {
        "id": "jordan",
        "name": "Jordan Lee",
        "initials": "JL",
        "project": "Plant Growth Experiment",
        "progress": 35,
        "step": "Recording observations",
        "status": "Help requested",
        "needs_help": True,
    },
    {
        "id": "sam",
        "name": "Sam Rivera",
        "initials": "SR",
        "project": "My Community Story",
        "progress": 80,
        "step": "Final presentation",
        "status": "On track",
        "needs_help": False,
    },
    {
        "id": "taylor",
        "name": "Taylor Brooks",
        "initials": "TB",
        "project": "Build a Simple Circuit",
        "progress": 20,
        "step": "Identifying materials",
        "status": "In progress",
        "needs_help": False,
    },
]


def show_classroom():
    st.title("Classroom Overview")
    st.caption(
        "Your students, their current projects, and learning progress."
    )

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Students", len(STUDENTS))

    with col2:
        st.metric("Active Projects", len(STUDENTS))

    with col3:
        st.metric(
            "Help Requests",
            sum(s["needs_help"] for s in STUDENTS)
        )

    st.divider()

    # Search
    search = st.text_input(
        "Search students or projects",
        placeholder="Search by name or project..."
    )

    filtered = [
        s for s in STUDENTS
        if search.lower() in (
            s["name"] + " " + s["project"]
        ).lower()
    ]

    # Student cards
    for i in range(0, len(filtered), 2):
        columns = st.columns(2, gap="large")

        for col, student in zip(columns, filtered[i:i+2]):
            with col:
                with st.container(border=True):
                    st.markdown(
                        f"### 👤 {student['name']}"
                    )

                    st.caption("CURRENT PROJECT")
                    st.markdown(
                        f"**{student['project']}**"
                    )
                    st.caption(student["step"])

                    st.progress(student["progress"] / 100)
                    st.caption(
                        f"{student['progress']}% complete"
                    )

                    if student["needs_help"]:
                        st.warning("⚠️ Help requested")
                    else:
                        st.success(student["status"])

                    left, right = st.columns(2)

                    with left:
                        if st.button(
                            "View Profile",
                            key=f"profile_{student['id']}",
                            use_container_width=True
                        ):
                            st.session_state["selected_student"] = student
                            st.session_state["teacher_page"] = "student_detail"
                            st.rerun()

                    with right:
                        if st.button(
                            "View Project",
                            key=f"project_{student['id']}",
                            use_container_width=True
                        ):
                            st.session_state["selected_student"] = student
                            st.session_state["teacher_page"] = "project_detail"
                            st.rerun()


def show_student_detail():
    student = st.session_state.get("selected_student")

    if not student:
        st.warning("No student selected.")
        return

    if st.button("← Back to Classroom"):
        st.session_state["teacher_page"] = "classroom"
        st.rerun()

    st.title(student["name"])
    st.caption("Student Learning Profile")

    categories = [
        "Currently Learning",
        "Interests",
        "Strengths",
        "Struggles",
        "Supports",
        "Notes"
    ]

    for category in categories:
        with st.expander(category, expanded=True):
            st.caption("Generated student insights")
            st.info("Student insights will appear here.")

            st.caption("Teacher observations")
            st.text_area(
                "Add your notes",
                key=f"notes_{student['id']}_{category}"
            )


def show_project_detail():
    student = st.session_state.get("selected_student")

    if not student:
        st.warning("No project selected.")
        return

    if st.button("← Back to Classroom"):
        st.session_state["teacher_page"] = "classroom"
        st.rerun()

    st.title(student["project"])
    st.caption(f"Assigned to {student['name']}")

    st.subheader("Current Progress")
    st.progress(student["progress"] / 100)
    st.write(f"Current step: {student['step']}")

    st.subheader("Project Summary")
    st.info("AI-generated project summaries will appear here.")

    st.subheader("Learning Checks")
    st.info("Comprehension results will appear here.")

    st.subheader("Teacher Assistance")

    if student["needs_help"]:
        st.warning("This student has requested assistance.")
    else:
        st.success("No active assistance requests.")
