"""
devtrack_file_manager.py
-------------------------
Domain: DevTrack Pro - Client Records Management

This module contains ONLY the file-handling logic (Lab 7 core requirement):
    - create_file()      -> mode 'w'
    - read_all_records()  -> mode 'r'
    - append_record()    -> mode 'a'
    - search_record()    -> mode 'r'   (readline + tell)
    - update_record()    -> mode 'r+'  (seek + writelines + truncate)
    - delete_record()    -> mode 'w'   (rewrite filtered file)
    - backup_file()      -> mode 'w+'  (write then read back to verify)

Each record is stored as a single pipe-delimited ('|') line in a plain
text file:  ID|Name|Email|Phone|ProjectCode|JoinDate|Status

Kept separate from the Streamlit GUI file for modular programming practice.
"""

import re
import os
import shutil

FIELDS = ["ID", "Name", "Email", "Phone", "ProjectCode", "JoinDate", "Status"]
DELIM = "|"


# ---------------------------------------------------------------
# CUSTOM EXCEPTIONS (Programming Requirement: exception handling)
# ---------------------------------------------------------------
class RecordNotFoundError(Exception):
    """Raised when a search/update/delete key does not match any record."""
    pass


class DuplicateRecordError(Exception):
    """Raised when trying to append a record with an ID that already exists."""
    pass


class InvalidRecordError(Exception):
    """Raised when a stored line does not have the expected number of fields."""
    pass


# ---------------------------------------------------------------
# REGEX VALIDATION FUNCTIONS (Requirement 5)
# ---------------------------------------------------------------
def validate_id(client_id):
    return bool(re.fullmatch(r"CLT\d{3}", client_id.strip().upper()))


def validate_name(name):
    return bool(re.fullmatch(r"[A-Za-z]+(?:\s[A-Za-z]+)+", name.strip()))


def validate_email(email):
    return bool(re.fullmatch(r"[\w.\-]+@[\w\-]+\.[A-Za-z]{2,}", email.strip()))


def validate_phone(phone):
    return bool(re.fullmatch(r"[6-9]\d{9}", phone.strip()))


def validate_project_code(code):
    return bool(re.fullmatch(r"DEV-\d{3}", code.strip().upper()))


def validate_date(date_str):
    # Expected format: DD-MM-YYYY
    return bool(re.fullmatch(r"(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-\d{4}", date_str.strip()))


def validate_record_fields(id_, name, email, phone, code, date):
    """Runs all field validators together and returns (is_valid, list_of_errors)."""
    errors = []
    if not validate_id(id_):
        errors.append("ID must look like 'CLT001' (CLT + 3 digits).")
    if not validate_name(name):
        errors.append("Name must contain only letters and at least one space (e.g. 'Ravi Kumar').")
    if not validate_email(email):
        errors.append("Email format is invalid (e.g. name@example.com).")
    if not validate_phone(phone):
        errors.append("Phone must be a 10-digit Indian mobile number starting with 6-9.")
    if not validate_project_code(code):
        errors.append("Project Code must look like 'DEV-101' (DEV- + 3 digits).")
    if not validate_date(date):
        errors.append("Date must be in DD-MM-YYYY format (e.g. 05-03-2025).")
    return (len(errors) == 0, errors)


# ---------------------------------------------------------------
# FILE HANDLING FUNCTIONS (Requirement 2, 3, 4)
# ---------------------------------------------------------------
def create_file(filepath, initial_records):
    """
    Creates (or overwrites) the data file with a starting set of records.
    File mode: 'w'  |  Methods used: writelines(), close()
    """
    try:
        f = open(filepath, 'w')          # mode 'w' -> create/overwrite
        lines = [DELIM.join(r) + "\n" for r in initial_records]
        f.writelines(lines)              # write() family: writelines()
        f.close()                        # explicit close()
        return True, f"File created successfully with {len(initial_records)} record(s)."
    except OSError as e:
        return False, f"Error creating file: {e}"


def read_all_records(filepath):
    """
    Reads and returns every record in the file as a list of dicts.
    File mode: 'r'  |  Methods used: readlines()
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file '{filepath}' does not exist. Please create it first.")

    with open(filepath, 'r') as f:       # mode 'r'
        lines = f.readlines()            # readlines()

    records = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(DELIM)
        if len(parts) != len(FIELDS):
            raise InvalidRecordError(f"Corrupted record line: {line}")
        records.append(dict(zip(FIELDS, parts)))
    return records


def append_record(filepath, record: dict):
    """
    Appends a new record to the end of the file without disturbing existing data.
    File mode: 'a'  |  Methods used: write()
    """
    try:
        # Prevent duplicate IDs
        existing = read_all_records(filepath)
        if any(r["ID"].upper() == record["ID"].upper() for r in existing):
            raise DuplicateRecordError(f"A record with ID '{record['ID']}' already exists.")

        line = DELIM.join(record[field] for field in FIELDS)
        with open(filepath, 'a') as f:   # mode 'a'
            f.write(line + "\n")         # write()
        return True, f"Record '{record['ID']}' appended successfully."
    except (DuplicateRecordError, FileNotFoundError) as e:
        return False, str(e)
    except OSError as e:
        return False, f"Error appending record: {e}"


def search_record(filepath, key_id):
    """
    Searches for a record by ID, reading line by line.
    File mode: 'r'  |  Methods used: readline(), tell()
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file '{filepath}' does not exist.")

    with open(filepath, 'r') as f:        # mode 'r'
        while True:
            position = f.tell()           # tell() -> current byte offset
            line = f.readline()           # readline() -> one line at a time
            if not line:                  # EOF reached
                break
            stripped = line.strip()
            if not stripped:
                continue
            parts = stripped.split(DELIM)
            if parts[0].upper() == key_id.strip().upper():
                record = dict(zip(FIELDS, parts))
                record["_file_position"] = position   # proof seek/tell was tracked
                return record
    return None  # not found


def update_record(filepath, key_id, updated_fields: dict):
    """
    Updates an existing record in place.
    File mode: 'r+'  |  Methods used: readlines(), seek(), writelines(), truncate()
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file '{filepath}' does not exist.")

    with open(filepath, 'r+') as f:       # mode 'r+' (read + write, no truncate on open)
        lines = f.readlines()             # readlines()
        found = False
        new_lines = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            parts = stripped.split(DELIM)
            if parts[0].upper() == key_id.strip().upper():
                record = dict(zip(FIELDS, parts))
                record.update(updated_fields)
                new_line = DELIM.join(record[field] for field in FIELDS) + "\n"
                new_lines.append(new_line)
                found = True
            else:
                new_lines.append(stripped + "\n")

        if not found:
            raise RecordNotFoundError(f"No record found with ID '{key_id}'.")

        f.seek(0)                         # seek() -> rewind to start of file
        f.writelines(new_lines)           # writelines()
        f.truncate()                      # remove any leftover old content

    return True, f"Record '{key_id}' updated successfully."


def delete_record(filepath, key_id):
    """
    Deletes a record by ID by rewriting the file without it.
    File mode: 'r' then 'w'  |  Methods used: readlines(), writelines()
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file '{filepath}' does not exist.")

    with open(filepath, 'r') as f:        # mode 'r'
        lines = f.readlines()             # readlines()

    new_lines = [
        line for line in lines
        if line.strip() and line.strip().split(DELIM)[0].upper() != key_id.strip().upper()
    ]

    if len(new_lines) == len(lines):
        raise RecordNotFoundError(f"No record found with ID '{key_id}'.")

    with open(filepath, 'w') as f:        # mode 'w' -> overwrite with filtered data
        f.writelines(new_lines)           # writelines()

    return True, f"Record '{key_id}' deleted successfully."


def backup_file(filepath, backup_path):
    """
    Creates a verified backup copy of the data file.
    File mode: 'r' then 'w+'  |  Methods used: read(), write(), seek(), read()
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file '{filepath}' does not exist.")

    with open(filepath, 'r') as src:      # mode 'r'
        content = src.read()              # read() -> whole file as one string

    with open(backup_path, 'w+') as bkp:  # mode 'w+' (write + read)
        bkp.write(content)                # write()
        bkp.seek(0)                       # seek() back to start
        verification = bkp.read()         # read() again to confirm it was written correctly

    if verification != content:
        return False, "Backup verification failed - contents do not match."

    record_count = len([l for l in content.splitlines() if l.strip()])
    return True, f"Backup created at '{backup_path}' with {record_count} record(s) verified."