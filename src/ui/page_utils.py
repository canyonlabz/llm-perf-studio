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
    filenames = [f for f in os.listdir(folder_path) if f.lower().endswith('.jmx')]
    selected_filename = st.selectbox(
        'Select a JMeter JMX file', 
        filenames,
        index=None,  # No default selection
        placeholder="Select a JMX file"
    )
    # If no files are found, return None
    if not selected_filename:
        st.warning("No JMX files selected.")
        return None
    # Return the full path of the selected file
    st.info(f"Selected JMX file: {selected_filename}")
    return os.path.join(folder_path, selected_filename) if filenames else None
