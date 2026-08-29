"""
lab_7_streamlit.py
--------------------
Domain: DevTrack Pro - Client Records Management System

Streamlit GUI layer only. All file handling / regex validation logic
lives in devtrack_file_manager.py (modular programming practice).
"""

import streamlit as st
import pandas as pd
import os
import devtrack_file_manager as fm

DATA_FILE = os.path.join(os.path.dirname(__file__), "clients_data.txt")
BACKUP_FILE = os.path.join(os.path.dirname(__file__), "clients_data_backup.txt")

STATUS_OPTIONS = ["Active", "On Hold", "Completed", "Inactive"]

st.set_page_config(page_title="DevTrack Pro | Client Records", page_icon="🗃️", layout="wide")

# ---------------------------------------------------------------
# Ensure the data file exists with at least 8 starting records
# ---------------------------------------------------------------
def ensure_initial_data():
    if not os.path.exists(DATA_FILE):
        initial_records = [
            ["CLT001", "Ravi Kumar",    "ravi.kumar@gmail.com",    "9845012345", "DEV-101", "01-01-2025", "Active"],
            ["CLT002", "Sneha Rao",     "sneha.rao@yahoo.com",     "9900123456", "DEV-102", "15-01-2025", "Active"],
            ["CLT003", "Arjun Mehta",   "arjun.mehta@outlook.com", "9876543210", "DEV-103", "20-02-2025", "On Hold"],
            ["CLT004", "Divya Shetty",  "divya.shetty@gmail.com",  "9123456789", "DEV-104", "05-03-2025", "Active"],
            ["CLT005", "Karthik Iyer",  "karthik.iyer@gmail.com",  "9988776655", "DEV-105", "18-03-2025", "Completed"],
            ["CLT006", "Priya Nair",    "priya.nair@hotmail.com",  "9012345678", "DEV-106", "02-04-2025", "Active"],
            ["CLT007", "Rahul Verma",   "rahul.verma@gmail.com",   "9765432109", "DEV-107", "22-04-2025", "Inactive"],
            ["CLT008", "Ananya Das",    "ananya.das@gmail.com",    "9871234560", "DEV-108", "10-05-2025", "Active"],
        ]
        fm.create_file(DATA_FILE, initial_records)

ensure_initial_data()

# ---------------------------------------------------------------
# SIDEBAR - quick stats
# ---------------------------------------------------------------
st.sidebar.title("DevTrack_ File Manager")
st.sidebar.caption("Domain: Client Records")

try:
    all_records = fm.read_all_records(DATA_FILE)
    st.sidebar.metric("Total Client Records", len(all_records))
except Exception as e:
    all_records = []
    st.sidebar.error(f"Could not load records: {e}")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**File:** `clients_data.txt`  \n"
    "**Format:** `ID|Name|Email|Phone|ProjectCode|JoinDate|Status`"
)

st.title("🗃️ DevTrack Pro — Client Records File Manager")
st.write("A domain-specific file handling application: create, read, append, search, update, delete, and back up client records stored in a plain text file.")

tabs = st.tabs(["📋 View Records", "➕ Add Record", "🔍 Search", "✏️ Update", "🗑️ Delete", "💾 Backup"])

# ---------------------------------------------------------------
# TAB 1: VIEW ALL RECORDS
# ---------------------------------------------------------------
with tabs[0]:
    st.subheader("All Client Records")
    try:
        records = fm.read_all_records(DATA_FILE)
        if records:
            df = pd.DataFrame(records)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No records found in the file yet.")
    except FileNotFoundError as e:
        st.error(str(e))
    except fm.InvalidRecordError as e:
        st.error(f"Data file appears corrupted: {e}")

# ---------------------------------------------------------------
# TAB 2: ADD RECORD (append_record -> mode 'a')
# ---------------------------------------------------------------
with tabs[1]:
    st.subheader("Add a New Client Record")
    with st.form("add_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            in_id = st.text_input("Client ID", placeholder="CLT009")
            in_name = st.text_input("Full Name", placeholder="Ravi Kumar")
            in_email = st.text_input("Email", placeholder="name@example.com")
            in_phone = st.text_input("Phone Number", placeholder="9876543210")
        with c2:
            in_code = st.text_input("Project Code", placeholder="DEV-109")
            in_date = st.text_input("Join Date (DD-MM-YYYY)", placeholder="05-06-2025")
            in_status = st.selectbox("Status", STATUS_OPTIONS)

        add_submitted = st.form_submit_button("Add Record")

    if add_submitted:
        is_valid, errors = fm.validate_record_fields(in_id, in_name, in_email, in_phone, in_code, in_date)
        if not is_valid:
            st.error("Please fix the following before submitting:")
            for err in errors:
                st.markdown(f"- {err}")
        else:
            new_record = {
                "ID": in_id.strip().upper(),
                "Name": in_name.strip(),
                "Email": in_email.strip(),
                "Phone": in_phone.strip(),
                "ProjectCode": in_code.strip().upper(),
                "JoinDate": in_date.strip(),
                "Status": in_status,
            }
            try:
                success, message = fm.append_record(DATA_FILE, new_record)
                if success:
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
            except Exception as e:
                st.error(f"Unexpected error while adding record: {e}")

# ---------------------------------------------------------------
# TAB 3: SEARCH (search_record -> readline + tell)
# ---------------------------------------------------------------
with tabs[2]:
    st.subheader("Search for a Client Record")
    search_id = st.text_input("Enter Client ID to search", placeholder="CLT003", key="search_box")
    if st.button("Search"):
        if not fm.validate_id(search_id):
            st.error("Please enter a valid Client ID in the format CLT001.")
        else:
            try:
                result = fm.search_record(DATA_FILE, search_id)
                if result:
                    pos = result.pop("_file_position")
                    st.success(f"✅ Record found (located at byte offset {pos} in the file):")
                    st.table(pd.DataFrame([result]))
                else:
                    st.warning(f"No record found with ID '{search_id}'.")
            except FileNotFoundError as e:
                st.error(str(e))

# ---------------------------------------------------------------
# TAB 4: UPDATE (update_record -> mode 'r+')
# ---------------------------------------------------------------
with tabs[3]:
    st.subheader("Update an Existing Record")
    update_id = st.text_input("Client ID to update", placeholder="CLT002", key="update_box")

    existing = None
    if update_id:
        try:
            existing = fm.search_record(DATA_FILE, update_id)
        except FileNotFoundError as e:
            st.error(str(e))

    if update_id and not existing:
        st.warning(f"No record found with ID '{update_id}'. Search will run once you finish typing a valid ID.")

    if existing:
        st.info(f"Editing record for **{existing['Name']}**")
        with st.form("update_form"):
            u_col1, u_col2 = st.columns(2)
            with u_col1:
                u_email = st.text_input("Email", value=existing["Email"])
                u_phone = st.text_input("Phone Number", value=existing["Phone"])
            with u_col2:
                u_code = st.text_input("Project Code", value=existing["ProjectCode"])
                u_status = st.selectbox("Status", STATUS_OPTIONS, index=STATUS_OPTIONS.index(existing["Status"]) if existing["Status"] in STATUS_OPTIONS else 0)

            update_submitted = st.form_submit_button("Update Record")

        if update_submitted:
            errs = []
            if not fm.validate_email(u_email):
                errs.append("Email format is invalid.")
            if not fm.validate_phone(u_phone):
                errs.append("Phone must be a valid 10-digit number starting with 6-9.")
            if not fm.validate_project_code(u_code):
                errs.append("Project Code must look like DEV-101.")

            if errs:
                st.error("Please fix the following:")
                for e in errs:
                    st.markdown(f"- {e}")
            else:
                try:
                    success, message = fm.update_record(
                        DATA_FILE, update_id,
                        {"Email": u_email.strip(), "Phone": u_phone.strip(),
                         "ProjectCode": u_code.strip().upper(), "Status": u_status}
                    )
                    st.success(f"✅ {message}")
                    st.rerun()
                except fm.RecordNotFoundError as e:
                    st.error(f"❌ {e}")
                except Exception as e:
                    st.error(f"Unexpected error while updating: {e}")

# ---------------------------------------------------------------
# TAB 5: DELETE (delete_record -> mode 'w')
# ---------------------------------------------------------------
with tabs[4]:
    st.subheader("Delete a Client Record")
    delete_id = st.text_input("Client ID to delete", placeholder="CLT005", key="delete_box")
    confirm = st.checkbox("I confirm I want to permanently delete this record.")

    if st.button("Delete Record"):
        if not delete_id:
            st.error("Please enter a Client ID.")
        elif not confirm:
            st.warning("Please check the confirmation box before deleting.")
        else:
            try:
                success, message = fm.delete_record(DATA_FILE, delete_id)
                st.success(f"✅ {message}")
                st.rerun()
            except fm.RecordNotFoundError as e:
                st.error(f"❌ {e}")
            except FileNotFoundError as e:
                st.error(str(e))

# ---------------------------------------------------------------
# TAB 6: BACKUP (backup_file -> mode 'w+')
# ---------------------------------------------------------------
with tabs[5]:
    st.subheader("Create a Backup Copy of the Data File")
    st.write("This reads the current data file and writes a verified backup copy (`clients_data_backup.txt`).")

    if st.button("Create Backup Now"):
        try:
            success, message = fm.backup_file(DATA_FILE, BACKUP_FILE)
            if success:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
        except FileNotFoundError as e:
            st.error(str(e))

    if os.path.exists(BACKUP_FILE):
        with st.expander("View current backup file contents"):
            try:
                backup_records = fm.read_all_records(BACKUP_FILE)
                st.dataframe(pd.DataFrame(backup_records), use_container_width=True)
            except Exception as e:
                st.error(f"Could not read backup file: {e}")

st.caption("DevTrack Pro — Client Records managed with pure Python file handling (open/read/write/seek/tell).")