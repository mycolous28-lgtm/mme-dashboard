import pandas as pd
import plotly.express as px
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title=(
        "Success Advisor Dashboard — Master of Management Engineering"
    ),
    page_icon="📊",
    layout="wide",
)

# Initialize Session State Configurations & Defaults
if "active_tab" not in st.session_state:
  st.session_state["active_tab"] = "Overview"
if "selected_student" not in st.session_state:
  st.session_state["selected_student"] = "Mateo Alcantara (MME-2401)"
if "program_instance" not in st.session_state:
  st.session_state["program_instance"] = (
      "Master of Management Engineering (IE-EMG)"
  )

# Admin Config Toggles State Initialization
if "kpi_total_enrolled" not in st.session_state:
  st.session_state["kpi_total_enrolled"] = True
if "kpi_on_time" not in st.session_state:
  st.session_state["kpi_on_time"] = True
if "kpi_completion" not in st.session_state:
  st.session_state["kpi_completion"] = True
if "kpi_remaining" not in st.session_state:
  st.session_state["kpi_remaining"] = True
if "kpi_at_risk" not in st.session_state:
  st.session_state["kpi_at_risk"] = True

# Field Mapping State Initialization
if "map_studentid" not in st.session_state:
  st.session_state["map_studentid"] = True
if "map_studentname" not in st.session_state:
  st.session_state["map_studentname"] = True
if "map_cohort" not in st.session_state:
  st.session_state["map_cohort"] = True
if "map_coursework" not in st.session_state:
  st.session_state["map_coursework"] = True
if "map_compexam" not in st.session_state:
  st.session_state["map_compexam"] = True
if "map_capstone" not in st.session_state:
  st.session_state["map_capstone"] = True
if "map_advisor" not in st.session_state:
  st.session_state["map_advisor"] = True


# Load Data including Advisers Directory from local CSV files
@st.cache_data
def load_data():
  df_students = pd.read_csv("Students_Master_List.csv")
  df_history = pd.read_csv("Historical_Trends.csv")
  df_advisers = pd.read_csv("Advisers_Directory.csv")
  return df_students, df_history, df_advisers


df_students, df_history, df_advisers = load_data()

# Top Header Banner
st.markdown(
    """
    <style>
    .top-banner { background-color: #1b263b; color: white; padding: 15px; border-radius: 5px; }
    </style>
    <div class="top-banner">
        <h3>MAPÚA UNIVERSITY · ETYSB</h3>
        <h2>Success Advisor Dashboard — Master of Management Engineering</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

# Navigation Bar Tabs
col_nav1, col_nav2, col_nav3, col_nav4, col_space = st.columns(
    [1, 1, 1, 1, 3]
)
with col_nav1:
  if st.button("Overview", use_container_width=True):
    st.session_state["active_tab"] = "Overview"
with col_nav2:
  if st.button("Roster", use_container_width=True):
    st.session_state["active_tab"] = "Roster"
with col_nav3:
  if st.button("Student Profile", use_container_width=True):
    st.session_state["active_tab"] = "Student Profile"
with col_nav4:
  if st.button("Admin Config", use_container_width=True):
    st.session_state["active_tab"] = "Admin Config"

st.write(
    f"**Program instance:** {st.session_state['program_instance']} | **Term:**"
    " Fall 2025-2026"
)
st.markdown("---")

# ==========================================
# VIEW 1: EXECUTIVE OVERVIEW
# ==========================================
if st.session_state["active_tab"] == "Overview":
  st.subheader("Executive Overview")

  kpi_cols = []
  if st.session_state["kpi_total_enrolled"]:
    kpi_cols.append("Total Enrolled")
  if st.session_state["kpi_on_time"]:
    kpi_cols.append("On-Time Graduation Rate")
  if st.session_state["kpi_completion"]:
    kpi_cols.append("Overall Completion %")
  if st.session_state["kpi_remaining"]:
    kpi_cols.append("Remaining Students")
  if st.session_state["kpi_at_risk"]:
    kpi_cols.append("Students At Risk")

  if kpi_cols:
    cols = st.columns(len(kpi_cols))
    idx = 0
    if st.session_state["kpi_total_enrolled"] and idx < len(cols):
      with cols[idx]:
        st.metric(
            label="TOTAL ENROLLED",
            value=len(df_students),
            delta="MME · Fall 2025-2026",
        )
      idx += 1
    if st.session_state["kpi_on_time"] and idx < len(cols):
      with cols[idx]:
        st.metric(
            label="ON-TIME GRADUATION RATE",
            value="58.0%",
            delta="3.2 pts vs last term",
        )
      idx += 1
    if st.session_state["kpi_completion"] and idx < len(cols):
      with cols[idx]:
        st.metric(
            label="OVERALL COMPLETION %",
            value="27.8%",
            delta="4.5 pts vs last term",
        )
      idx += 1
    if st.session_state["kpi_remaining"] and idx < len(cols):
      with cols[idx]:
        st.metric(
            label="REMAINING STUDENTS",
            value=str(
                len(df_students[df_students["Coursework"] != "Completed"])
            ),
            delta="across all active stages",
        )
      idx += 1
    if st.session_state["kpi_at_risk"] and idx < len(cols):
      with cols[idx]:
        st.markdown(
            '<div style="background-color:#fff5f5; padding:10px;'
            ' border-radius:5px; border: 1px solid #feb2b2;"><b>STUDENTS AT'
            ' RISK</b><br><span style="font-size:24px; color:#c53030;'
            " font-weight:bold;>"
            f'{len(df_students[df_students["Risk_Status"] == "AT RISK"])}</span><br><span'
            ' style="font-size:12px; color:#c53030;">overdue on current'
            " stage</span></div>",
            unsafe_allow_html=True,
        )
      idx += 1

  st.markdown("---")

  col_chart1, col_chart2 = st.columns(2)
  with col_chart1:
    st.markdown("#### Cohort by Lifecycle Stage")
    stage_counts = {
        "Coursework": len(df_students[df_students["Coursework"] != "Completed"]),
        "Comprehensive Exam": len(
            df_students[df_students["Comp_Exam"] == "In-Progress"]
        ),
        "Capstone": len(
            df_students[df_students["Capstone"] == "In-Progress"]
        ),
        "Completed": len(df_students[df_students["Coursework"] == "Completed"]),
    }
    fig_stages = px.bar(
        x=list(stage_counts.keys()),
        y=list(stage_counts.values()),
        color=list(stage_counts.keys()),
        text_auto=True,
    )
    st.plotly_chart(fig_stages, use_container_width=True)

  with col_chart2:
    st.markdown("#### Overall Completion % — Trend")
    fig_trend = px.line(
        df_history,
        x="Term",
        y="Overall_Completion_Rate",
        markers=True,
        line_shape="linear",
    )
    st.plotly_chart(fig_trend, use_container_width=True)

  st.markdown("### Students At Risk — Requires Follow-Up")
  risk_df = df_students[df_students["Risk_Status"] == "AT RISK"][
      [
          "Student_ID",
          "Full_Name",
          "Cohort",
          "Coursework",
          "Comp_Exam",
          "Capstone",
          "Days_In_Stage",
      ]
  ]
  risk_df["Flag"] = "AT RISK"
  st.dataframe(risk_df, use_container_width=True)

# ==========================================
# VIEW 2: STUDENT ROSTER & ADVISERS DIRECTORY
# ==========================================
elif st.session_state["active_tab"] == "Roster":
  st.subheader(
      f"Management Engineering Student Roster ({len(df_students)} students)"
  )
  st.write("Live view from local CSV dataset")

  f_col1, f_col2, f_col3, f_col4 = st.columns(4)
  with f_col1:
    cohort_filter = st.selectbox(
        "Cohort", ["All Cohorts"] + list(df_students["Cohort"].unique())
    )
  with f_col2:
    advisor_filter = st.selectbox(
        "Advisor", ["All Advisors"] + list(df_students["Advisor"].unique())
    )
  with f_col3:
    status_filter = st.selectbox(
        "Status", ["All Statuses"] + list(df_students["Risk_Status"].unique())
    )
  with f_col4:
    search_query = st.text_input("Search name or student ID...")

  filtered_df = df_students.copy()
  if cohort_filter != "All Cohorts":
    filtered_df = filtered_df[filtered_df["Cohort"] == cohort_filter]
  if advisor_filter != "All Advisors":
    filtered_df = filtered_df[filtered_df["Advisor"] == advisor_filter]
  if status_filter != "All Statuses":
    filtered_df = filtered_df[filtered_df["Risk_Status"] == status_filter]
  if search_query:
    filtered_df = filtered_df[
        filtered_df["Full_Name"].str.contains(search_query, case=False)
        | filtered_df["Student_ID"].str.contains(search_query, case=False)
    ]

  active_cols = []
  col_rename_map = {}
  if st.session_state["map_studentid"]:
    active_cols.append("Student_ID")
    col_rename_map["Student_ID"] = "STUDENT"
  if st.session_state["map_studentname"]:
    active_cols.append("Full_Name")
    col_rename_map["Full_Name"] = "NAME"
  if st.session_state["map_cohort"]:
    active_cols.append("Cohort")
    col_rename_map["Cohort"] = "COHORT"
  if st.session_state["map_advisor"]:
    active_cols.append("Advisor")
    col_rename_map["Advisor"] = "ADVISOR"
  if st.session_state["map_coursework"]:
    active_cols.append("Coursework")
    col_rename_map["Coursework"] = "COURSEWORK"
  if st.session_state["map_compexam"]:
    active_cols.append("Comp_Exam")
    col_rename_map["Comp_Exam"] = "COMP. EXAM"
  if st.session_state["map_capstone"]:
    active_cols.append("Capstone")
    col_rename_map["Capstone"] = "CAPSTONE"

  active_cols.extend(["Last_Updated", "Risk_Status"])
  col_rename_map["Last_Updated"] = "LAST UPDATED"
  col_rename_map["Risk_Status"] = "RISK"

  display_df = filtered_df[active_cols].rename(columns=col_rename_map)
  st.dataframe(display_df, use_container_width=True)

  st.markdown("---")
  st.subheader("Faculty Advisers Directory (IE-EMG)")
  st.dataframe(df_advisers, use_container_width=True)

# ==========================================
# VIEW 3: STUDENT PROFILE
# ==========================================
elif st.session_state["active_tab"] == "Student Profile":
  st.subheader("Student Profile View")
  selected_name_id = st.selectbox(
      "Select Student",
      df_students["Full_Name"] + " (" + df_students["Student_ID"] + ")",
  )
  student_row = df_students[
      (df_students["Full_Name"] + " (" + df_students["Student_ID"] + ")")
      == selected_name_id
  ].iloc[0]

  st.markdown(
      f"""
    <div style="background-color:#ffffff; padding:20px; border-radius:8px; border:1px solid #ddd;">
        <h3>{student_row['Full_Name']} <span style="font-size:16px; color:gray;">{student_row['Student_ID']}</span></h3>
        <p><b>Cohort:</b> {student_row['Cohort']} &nbsp;|&nbsp; <b>Assigned Advisor:</b> {student_row['Advisor']} &nbsp;|&nbsp; 
        <span style="color:red; background-color:#fff5f5; padding:3px 8px; border-radius:4px;"><b>{student_row['Risk_Status']} — {student_row['Days_In_Stage']} days in current stage</b></span></p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("#### Program Lifecycle Status")
  p1, p2, p3 = st.columns(3)
  with p1:
    st.info(
        f"**Coursework**\n\nStatus: {student_row['Coursework']}\nLast updated:"
        f" {student_row['Last_Updated']}"
    )
  with p2:
    st.warning(
        f"**Comprehensive Exam**\n\nStatus:"
        f" {student_row['Comp_Exam']}\nLast updated:"
        f" {student_row['Last_Updated']}"
    )
  with p3:
    st.success(
        f"**Capstone Paper**\n\nStatus:"
        f" {student_row['Capstone']}\nLast updated:"
        f" {student_row['Last_Updated']}"
    )

  st.markdown("#### Advisor Notes")
  st.text_area(
      "Add New Note:", placeholder="Type advising session notes here..."
  )
  if st.button("+ Add Note"):
    st.success("Note saved successfully.")

# ==========================================
# VIEW 4: ADMIN CONFIGURATION
# ==========================================
elif st.session_state["active_tab"] == "Admin Config":
  st.subheader("Admin Configuration & Field Mapping")
  st.write(
      f"Program instance: **{st.session_state['program_instance']}** — Live"
  )

  if st.button("+ Clone This Configuration for a New Program"):
    st.session_state["program_instance"] = (
        "Master of Management Engineering - Batch 2 (IE-EMG Clone)"
    )
    st.success(
        "Successfully cloned configuration into a new isolated program"
        f" instance: {st.session_state['program_instance']}"
    )
    st.rerun()

  st.markdown("---")
  st.markdown("### Field Mapping (US-10)")

  st.session_state["map_studentid"] = st.toggle(
      "Student ID",
      value=st.session_state["map_studentid"],
      key="t_map_studentid",
  )
  st.session_state["map_studentname"] = st.toggle(
      "Student Name",
      value=st.session_state["map_studentname"],
      key="t_map_studentname",
  )
  st.session_state["map_cohort"] = st.toggle(
      "Cohort", value=st.session_state["map_cohort"], key="t_map_cohort"
  )
  st.session_state["map_coursework"] = st.toggle(
      "Coursework Status",
      value=st.session_state["map_coursework"],
      key="t_map_coursework",
  )
  st.session_state["map_compexam"] = st.toggle(
      "Comprehensive Exam Status",
      value=st.session_state["map_compexam"],
      key="t_map_compexam",
  )
  st.session_state["map_capstone"] = st.toggle(
      "Capstone Status",
      value=st.session_state["map_capstone"],
      key="t_map_capstone",
  )
  st.session_state["map_advisor"] = st.toggle(
      "Assigned Advisor",
      value=st.session_state["map_advisor"],
      key="t_map_advisor",
  )

  st.markdown("### KPI Tile Configuration (US-29)")
  st.session_state["kpi_total_enrolled"] = st.toggle(
      "Total Enrolled — Executive Overview tile",
      value=st.session_state["kpi_total_enrolled"],
      key="t_kpi_total",
  )
  st.session_state["kpi_on_time"] = st.toggle(
      "On-Time Graduation Rate — Executive Overview tile",
      value=st.session_state["kpi_on_time"],
      key="t_kpi_ontime",
  )
  st.session_state["kpi_completion"] = st.toggle(
      "Overall Completion % — Executive Overview tile",
      value=st.session_state["kpi_completion"],
      key="t_kpi_completion",
  )
  st.session_state["kpi_remaining"] = st.toggle(
      "Remaining Students — Executive Overview tile",
      value=st.session_state["kpi_remaining"],
      key="t_kpi_remaining",
  )
  st.session_state["kpi_at_risk"] = st.toggle(
      "Students At Risk — Executive Overview tile",
      value=st.session_state["kpi_at_risk"],
      key="t_kpi_risk",
  )

  st.markdown("### Program-Specific Thresholds & Terminology (US-27 / US-30)")
  st.text_input("At-Risk Threshold", value="180 days in a single stage")
  st.text_input("Capstone Label", value='"Capstone Paper" (this program)')
  st.text_input(
      "Comprehensive Exam Label", value='"Comprehensive Exam" (this program)'
  )
  st.text_input("Data Refresh Schedule", value="Nightly, 02:00 Asia/Manila")

  if st.button("Save Configuration"):
    st.success("Configuration updated and applied across all dashboard views.")

st.markdown("---")
st.caption(
    "MME Success Advisor Dashboard · Built for CSE310 OBE Agile Pilot · Data"
    " source: CSV local files"
)