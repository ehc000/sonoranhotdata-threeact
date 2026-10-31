
import streamlit as st

from teacher.classroom import (
    show_classroom,
    show_student_detail,
    show_project_detail,
)
from teacher.help_requests import show_help_requests


def show_teacher_dashboard():

    if "teacher_page" not in st.session_state:
        st.session_state["teacher_page"] = "classroom"

    with st.sidebar:
        st.title("🎓 Adaptive Classroom")
        st.caption("Teacher Portal")
        st.divider()

        if st.button("🏠 Classroom Overview", use_container_width=True):
            st.session_state["teacher_page"] = "classroom"
            st.rerun()

        if st.button("✨ Project Generation", use_container_width=True):
            st.session_state["teacher_page"] = "project_generation"
            st.rerun()

        if st.button("🆘 Help Requests", use_container_width=True):
            st.session_state["teacher_page"] = "help_requests"
            st.rerun()

        st.divider()

        if st.button("👤 Teacher Profile", use_container_width=True):
            st.session_state["teacher_page"] = "teacher_profile"
            st.rerun()

        if st.button("← Switch Role", use_container_width=True):
            st.session_state.pop("role", None)
            st.session_state["teacher_page"] = "classroom"
            st.rerun()

    page = st.session_state["teacher_page"]

    if page == "classroom":
        show_classroom()

    elif page == "student_detail":
        show_student_detail()

    elif page == "project_detail":
        show_project_detail()

    elif page == "help_requests":
        show_help_requests()

    elif page == "project_generation":
        st.title("Project Generation")
        st.info("Project creator coming soon!")

    elif page == "teacher_profile":
        st.title("Teacher Profile")
        st.info("Teacher profile and avatar coming soon!")
