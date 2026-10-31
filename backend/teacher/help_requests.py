
import streamlit as st
from teacher.classroom import STUDENTS


def show_help_requests():
    st.title("Help Requests")
    st.caption("Students who have requested teacher assistance.")

    requests = [
        student for student in STUDENTS
        if student["needs_help"]
    ]

    st.metric("Active Help Requests", len(requests))
    st.divider()

    if not requests:
        st.success("No students are currently requesting help.")
        return

    for student in requests:
        with st.container(border=True):
            st.markdown(f"### 👤 {student['name']}")
            st.warning("Student requested assistance")

            st.markdown(
                f"**Current Project:** {student['project']}"
            )
            st.markdown(
                f"**Current Step:** {student['step']}"
            )

            st.progress(student["progress"] / 100)

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "View Student Profile",
                    key=f"help_profile_{student['id']}",
                    use_container_width=True,
                ):
                    st.session_state["selected_student"] = student
                    st.session_state["teacher_page"] = "student_detail"
                    st.rerun()

            with col2:
                if st.button(
                    "View Project",
                    key=f"help_project_{student['id']}",
                    use_container_width=True,
                ):
                    st.session_state["selected_student"] = student
                    st.session_state["teacher_page"] = "project_detail"
                    st.rerun()
