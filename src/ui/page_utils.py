'''
Module for utility functions related to UI pages.
'''
import os
from datetime import datetime
import streamlit as st

# Function to format a duration into a human-readable string
# Example: timedelta(minutes=5, seconds=30) -> "5 minutes, 30 seconds"
# Assume duration is a timedelta, start_time and end_time are datetime objects
def format_duration(duration):
    total_seconds = int(duration.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    parts = []
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return ", ".join(parts)

# Function to format a datetime object into a readable string
# Example: datetime(2023, 10, 5, 14, 30) -> "October 5, 2023 14:30:00 UTC"
def format_datetime(dt):
    # Use '%-d' on Unix, '%#d' on Windows for day without leading zero
    day_format = "%#d" if os.name == "nt" else "%-d"
    return dt.strftime(f"%B {day_format}, %Y %H:%M:%S UTC")

# Function to select a file from a given folder path
# This function lists all files with a .jmx extension in the specified folder
def file_selector(folder_path='.'):
    # Get list of JMX files
    filenames = [f for f in os.listdir(folder_path) if f.lower().endswith('.jmx')]
    if not filenames:
        st.warning("No JMX files found in the specified folder.")
        return None

    # Get current selection from session state or if not set set to None
    if 'selected_jmx_file' not in st.session_state:
        st.session_state.selected_jmx_file = None

    # Set default index to the previously selected file if it exists in the list
    default_index = None
    if st.session_state.selected_jmx_file and st.session_state.selected_jmx_file in filenames:
        default_index = filenames.index(st.session_state.selected_jmx_file)

    # Create selectbox with persisted state
    selected_filename = st.selectbox(
        'Select a JMeter JMX file', 
        filenames,
        key='jmx_file_selector',  # Unique key for the selectbox
        index=default_index,
        help="Select a JMX file to load. If no files are found, please ensure you have JMX files in the specified folder.",
        placeholder="Select a JMX file" if filenames else "No JMX files found"
    )

    # Update session state when selection changes
    if selected_filename and selected_filename != st.session_state.selected_jmx_file:
        st.session_state.selected_jmx_file = selected_filename

    if st.session_state.selected_jmx_file:
        full_path = os.path.join(folder_path, st.session_state.selected_jmx_file)
        st.session_state.jmeter_state.update({
            "jmx_path": full_path,
            "jmx_valid": os.path.exists(full_path)
        })
        st.info(f"Selected file: {selected_filename}")

        # Return the full path of the selected file
        return full_path
    else:
        st.warning("No JMX file selected.")
        return None

