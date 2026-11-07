import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Timetable Optimizer",
    page_icon="📅",
    layout="wide"
)

# Header
st.title("📅 School Timetable Optimizer")

st.caption(
    "An intelligent constraint-based school scheduling system."
)

st.divider()

# Overview
st.subheader("School Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Students", "90")
col2.metric("Teachers", "20")
col3.metric("Departments", "10")
col4.metric("Grades", "3")

st.divider()

# Navigation
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a section",
    [
        "Dashboard",
        "Students",
        "Teachers",
        "Courses",
        "Classrooms",
        "Optimization",
        "Timetable"
    ]
)

# Main content
if page == "Dashboard":

    st.header("Dashboard")

    st.info(
        "Welcome to the School Timetable Optimizer."
    )

    st.write(
        "Manage school resources and generate "
        "optimized weekly timetables."
    )

    st.subheader("System Status")

    st.success("Web interface initialized.")

    st.warning(
        "Scheduling engine is under development."
    )

elif page == "Students":
    st.header("Student Management")
    st.write("Student data management will be implemented here.")

elif page == "Teachers":
    st.header("Teacher Management")
    st.write("Teacher data management will be implemented here.")

elif page == "Courses":
    st.header("Course Management")
    st.write("Course management will be implemented here.")

elif page == "Classrooms":
    st.header("Classroom Management")
    st.write("Classroom management will be implemented here.")

elif page == "Optimization":
    st.header("Timetable Optimization")
    st.write("Optimization settings will be implemented here.")

elif page == "Timetable":
    st.header("Generated Timetable")
    st.write("Your optimized timetable will appear here.")
