
import streamlit as st
from teacher.dashboard import show_teacher_dashboard

st.set_page_config(
    page_title="Adaptive Classroom",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Global styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(
            135deg,
            #F8FAFF 0%,
            #EEF2FF 55%,
            #F6F0FF 100%
        );
        color: #24304A;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.92);
        border: 1px solid #E2E6F3;
        border-radius: 20px;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


def show_landing_page():

    st.markdown(
        "<h1 style='text-align:center; color:#242B4A;'>"
        "Learning, made for you."
        "</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center; color:#69738A;'>"
        "A different way to teach. A better way to learn."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    left, right = st.columns(2, gap="large")

    with left:
        with st.container(border=True):
            st.header("👩‍🏫 Teacher")
            st.write(
                "Create projects, guide instruction, "
                "and support every student."
            )

            if st.button(
                "Enter Teacher Portal",
                use_container_width=True
            ):
                st.session_state["role"] = "teacher"
                st.rerun()

    with right:
        with st.container(border=True):
            st.header("🎓 Student")
            st.write(
                "Explore projects and learn "
                "in a way that works for you."
            )

            if st.button(
                "Enter Student Portal",
                use_container_width=True
            ):
                st.session_state["role"] = "student"
                st.rerun()


# Role-based routing
role = st.session_state.get("role")

if role == "teacher":
    show_teacher_dashboard()

elif role == "student":
    st.title("Student Portal")
    st.info("Student interface coming soon!")

    if st.button("← Back to Role Selection"):
        st.session_state.pop("role", None)
        st.rerun()

else:
    show_landing_page()
