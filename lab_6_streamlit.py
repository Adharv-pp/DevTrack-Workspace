import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "projects_data.csv")

st.set_page_config(page_title="DevTrack Pro | Public Dashboard", page_icon="🗂️", layout="wide")

# ---------------------------------------------------------
# LOAD DATA (Lab 6: Create and use a CSV file to access data)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)

df = load_data()

# ---------------------------------------------------------
# SIDEBAR (Layout feature: Sidebar) — filters
# ---------------------------------------------------------
st.sidebar.title("DevTrack_ Dashboard")
st.sidebar.caption("Public project analytics portal")

st.sidebar.markdown("### Filters")

status_options = ["All"] + sorted(df["status"].unique().tolist())
selected_status = st.sidebar.selectbox("Filter by Status", status_options)          # select box

completed_only = st.sidebar.checkbox("Show only Completed projects")               # checkbox

min_hours = st.sidebar.slider(                                                     # slider
    "Minimum Hours Logged",
    min_value=0,
    max_value=int(df["hours_logged"].max()),
    value=0,
    step=5
)

search_term = st.sidebar.text_input("🔍 Search by Project Title")                   # text input (extra: live search)

chart_type = st.sidebar.radio("Chart Type", ["Bar Chart", "Line Chart", "Pie Chart"])  # radio button

# Apply filters
filtered_df = df.copy()
if selected_status != "All":
    filtered_df = filtered_df[filtered_df["status"] == selected_status]
if completed_only:
    filtered_df = filtered_df[filtered_df["status"] == "Completed"]
filtered_df = filtered_df[filtered_df["hours_logged"] >= min_hours]
if search_term.strip():
    filtered_df = filtered_df[filtered_df["title"].str.contains(search_term.strip(), case=False, na=False)]

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("🗂️ DevTrack Pro — Public Project Dashboard")
st.write("A read-only analytics view of the DevTrack project workspace, built with Streamlit, Pandas, and NumPy.")

# ---------------------------------------------------------
# METRICS ROW (Layout feature: Columns)
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

total_projects = len(filtered_df)
total_revenue = filtered_df["revenue"].sum()
avg_hours = np.mean(filtered_df["hours_logged"]) if total_projects > 0 else 0
std_hours = np.std(filtered_df["hours_logged"]) if total_projects > 0 else 0

col1.metric("Total Projects", total_projects)
col2.metric("Total Revenue", f"${total_revenue:,.0f}")
col3.metric("Avg. Hours Logged", f"{avg_hours:.1f}")
col4.metric("Std. Dev (Hours)", f"{std_hours:.1f}")

st.divider()

# ---------------------------------------------------------
# ADD NEW PROJECT (Container) — Lab 6: accept user input + display it
# ---------------------------------------------------------
with st.container(border=True):
    st.subheader("➕ Add a New Project")

    with st.form("add_project_form", clear_on_submit=True):
        f_col1, f_col2, f_col3 = st.columns(3)

        with f_col1:
            new_title = st.text_input("Project Title")                     # text input
            new_tech = st.text_input("Tech Stack")                         # text input

        with f_col2:
            new_status = st.selectbox("Status", ["Planning", "In Progress", "Training", "Completed"])  # select box
            new_hours = st.number_input("Hours Logged", min_value=0, max_value=1000, step=1)            # number input

        with f_col3:
            new_revenue = st.number_input("Revenue ($)", min_value=0, max_value=100000, step=100)        # number input

        submitted = st.form_submit_button("Add Project")                   # form-specific submit button

    if submitted:
        if not new_title.strip() or not new_tech.strip():
            st.error("Please fill in both Project Title and Tech Stack before submitting.")
        else:
            new_id = int(df["id"].max()) + 1 if not df.empty else 1
            new_row = pd.DataFrame([{
                "id": new_id,
                "title": new_title.strip(),
                "tech": new_tech.strip(),
                "status": new_status,
                "hours_logged": new_hours,
                "revenue": new_revenue
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(CSV_PATH, index=False)   
            load_data.clear()                  

            st.success(
                f"✅ Project added successfully!\n\n"
                f"**{new_title}** | Tech: {new_tech} | Status: {new_status} | "
                f"Hours: {new_hours} | Revenue: ${new_revenue:,.0f}"
            )
            st.rerun()

st.divider()

# ---------------------------------------------------------
# DATA TABLE (Lab 6: Display data using table or DataFrame)
# ---------------------------------------------------------
table_tab, chart_tab = st.tabs(["📋 Project Records", "📊 Visualisation"])

with table_tab:
    st.dataframe(filtered_df, use_container_width=True)

    # Extra: download the currently filtered view as CSV
    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download filtered data as CSV",
        data=csv_bytes,
        file_name="devtrack_filtered_projects.csv",
        mime="text/csv"
    )

    with st.expander("View Full Raw Dataset (unfiltered)"):                # Layout feature: Expander
        st.write(f"Total records in CSV: **{len(df)}**")
        st.dataframe(df, use_container_width=True)

# ---------------------------------------------------------
# CHART (Lab 6: Bar / Line / Pie chart)
# ---------------------------------------------------------
with chart_tab:
    if filtered_df.empty:
        st.warning("No records match the current filters — adjust them in the sidebar to see a chart.")
    else:
        chart_data = filtered_df.groupby("status")["hours_logged"].sum()

        if chart_type == "Bar Chart":
            st.bar_chart(chart_data)

        elif chart_type == "Line Chart":
            st.line_chart(filtered_df.set_index("title")["hours_logged"])

        elif chart_type == "Pie Chart":
            fig, ax = plt.subplots()
            ax.pie(chart_data, labels=chart_data.index, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
            st.pyplot(fig)

st.caption("DevTrack Pro — Streamlit dashboard reading live from projects_data.csv")