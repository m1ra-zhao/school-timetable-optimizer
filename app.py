import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Timetable Optimizer",
    page_icon="📅",
    layout="wide"
)

# --------------------------------
# 1. Data schemas
# --------------------------------

TABLES = {
    "Students": [
        "student_id",
        "grade",
        "homeroom"
    ],

    "Teachers": [
        "teacher_id",
        "department",
        "max_lessons_per_week"
    ],

    "Courses": [
        "section_id",
        "grade",
        "subject",
        "level",
        "lessons_per_week",
        "teacher_id",
        "room_type",
        "double_lesson_required"
    ],

    "Enrollments": [
        "student_id",
        "section_id"
    ],

    "Rooms": [
        "room_id",
        "room_type",
        "capacity",
        "building",
        "floor"
    ]
}

PRIMARY_KEYS = {
    "Students": "student_id",
    "Teachers": "teacher_id",
    "Courses": "section_id",
    "Rooms": "room_id"
}

# --------------------------------
# 2. Initialize session data
# --------------------------------

if "school_data" not in st.session_state:
    st.session_state.school_data = {
        name: pd.DataFrame(columns=columns)
        for name, columns in TABLES.items()
    }


# --------------------------------
# 3. Read uploaded files
# --------------------------------

def read_file(file):

    if file.name.endswith(".csv"):
        df = pd.read_csv(file, dtype=str)

    else:
        df = pd.read_excel(file, dtype=str)

    return df.fillna("")


# --------------------------------
# 4. Basic validation
# --------------------------------

def validate_table(name, df):

    issues = []

    if df.empty:
        issues.append("No data uploaded.")
        return issues

    required = TABLES[name]

    missing = [
        col for col in required
        if col not in df.columns
    ]

    if missing:
        issues.append(
            f"Missing columns: {missing}"
        )
        return issues

    if name in PRIMARY_KEYS:

        key = PRIMARY_KEYS[name]

        if df[key].duplicated().any():
            issues.append(
                f"Duplicate {key} found."
            )

    if name == "Enrollments":

        if df.duplicated(
            ["student_id", "section_id"]
        ).any():

            issues.append(
                "Duplicate enrollment records found."
            )

    if name == "Courses":

        values = pd.to_numeric(
            df["lessons_per_week"],
            errors="coerce"
        )

        if values.isna().any():
            issues.append(
                "Invalid lessons_per_week values."
            )

    return issues


# --------------------------------
# 5. Sidebar
# --------------------------------

st.sidebar.title("Timetable Optimizer")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Students",
        "Teachers",
        "Courses",
        "Enrollments",
        "Rooms",
        "Data Validation",
        "Optimization",
        "Timetable"
    ]
)


# --------------------------------
# 6. Dashboard
# --------------------------------

if page == "Dashboard":

    st.title("School Timetable Optimizer")

    st.caption(
        "Constraint-based scheduling and optimization"
    )

    st.divider()

    data = st.session_state.school_data

    cols = st.columns(5)

    names = [
        "Students",
        "Teachers",
        "Courses",
        "Enrollments",
        "Rooms"
    ]

    for col, name in zip(cols, names):

        col.metric(
            name,
            len(data[name])
        )

    st.divider()

    st.info(
        "Upload your school data to begin."
    )


# --------------------------------
# 7. Data management pages
# --------------------------------

elif page in TABLES:

    st.title(page + " Management")

    columns = TABLES[page]

    st.write(
        "Required fields:",
        ", ".join(columns)
    )

    st.divider()

    # Download template

    template = pd.DataFrame(columns=columns)

    st.download_button(
        "Download CSV Template",
        template.to_csv(index=False),
        file_name=f"{page.lower()}.csv",
        mime="text/csv"
    )

    # Upload file

    uploaded = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx"],
        key=f"upload_{page}"
    )

    if uploaded is not None:

        try:

            new_data = read_file(uploaded)

            missing = [
                col for col in columns
                if col not in new_data.columns
            ]

            if missing:

                st.error(
                    f"Missing required columns: {missing}"
                )

            else:

                st.session_state.school_data[
                    page
                ] = new_data

                st.success(
                    "Data uploaded successfully."
                )

        except Exception as e:

            st.error(f"Unable to read file: {e}")

    # Data preview

    st.subheader("Data Preview")

    df = st.session_state.school_data[page]

    if df.empty:

        st.info(
            "No data available. Upload a file to begin."
        )

    else:

        st.dataframe(
            df,
            use_container_width=True
        )

        st.caption(
            f"Total records: {len(df)}"
        )

        st.download_button(
            "Export Current Data",
            df.to_csv(index=False),
            file_name=f"{page.lower()}_export.csv",
            mime="text/csv"
        )

        if st.button(
            f"Clear {page} Data"
        ):

            st.session_state.school_data[
                page
            ] = pd.DataFrame(columns=columns)

            st.rerun()


# --------------------------------
# 8. Global data validation
# --------------------------------

elif page == "Data Validation":

    st.title("Data Validation")

    data = st.session_state.school_data

    all_issues = []

    for name, df in data.items():

        st.subheader(name)

        issues = validate_table(name, df)

        if issues:

            for issue in issues:
                st.error(issue)

            all_issues.extend(
                [f"{name}: {issue}" for issue in issues]
            )

        else:

            st.success(
                f"{len(df)} records loaded."
            )

    # Relationship validation

    students = data["Students"]
    teachers = data["Teachers"]
    courses = data["Courses"]
    enrollments = data["Enrollments"]

    if (
        not students.empty
        and not teachers.empty
        and not courses.empty
        and not enrollments.empty
    ):

        st.divider()

        st.subheader("Relationship Checks")

        student_ids = set(students["student_id"])
        teacher_ids = set(teachers["teacher_id"])
        section_ids = set(courses["section_id"])

        if not set(courses["teacher_id"]).issubset(
            teacher_ids
        ):

            st.error(
                "Some courses refer to unknown teachers."
            )

            all_issues.append(
                "Unknown teacher references."
            )

        else:

            st.success(
                "All course teachers exist."
            )

        if not set(enrollments["student_id"]).issubset(
            student_ids
        ):

            st.error(
                "Some enrollments refer to unknown students."
            )

            all_issues.append(
                "Unknown student references."
            )

        else:

            st.success(
                "All enrolled students exist."
            )

        if not set(enrollments["section_id"]).issubset(
            section_ids
        ):

            st.error(
                "Some enrollments refer to unknown courses."
            )

            all_issues.append(
                "Unknown course references."
            )

        else:

            st.success(
                "All enrolled courses exist."
            )

    st.divider()

    if all_issues:

        st.warning(
            f"Found {len(all_issues)} validation issues."
        )

    else:

        st.success(
            "No validation issues found in the available data."
        )


# --------------------------------
# 9. Future modules
# --------------------------------

elif page == "Optimization":

    st.title("Optimization")

    st.info(
        "The CP-SAT scheduling engine "
        "will be implemented in the next stage."
    )


elif page == "Timetable":

    st.title("Generated Timetable")

    st.info(
        "Generated schedules will appear here."
    )
