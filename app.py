import streamlit as st
import pandas as pd
from gpt_medical_info_extractor import get_processed_notes, extract_info_from_notes
from clinical_note import process_structured_info

# Set up the Streamlit page configuration
st.set_page_config(page_title="Clinical Notes Visualizer", layout="wide")

# Display the main title of the app
st.title("Clinical Notes Visualizer")

# Add a description of the app's functionality
st.markdown("""
This app is designed to process and visualize custom clinical notes. 
You can enter your own clinical note in the sidebar and process it using GPT.
Example notes are provided for testing purposes only.
""")

# Create a sidebar for user input and settings
st.sidebar.header("Settings")
# Allow user to input their OpenAI API key
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# Add a text area for users to input their own clinical notes
custom_note = st.sidebar.text_area("Enter your own clinical note", height=300, help="Enter your clinical note here for processing")

# Option to load example notes for testing
load_examples = st.sidebar.checkbox("Load example notes (for testing only)", value=False)
num_examples = st.sidebar.number_input("Number of example notes", min_value=1, max_value=10, value=2, disabled=not load_examples)

# Function to display a section of the clinical note
def display_section(title, content):
    st.subheader(title)
    if isinstance(content, dict):
        for key, value in content.items():
            st.write(f"**{key.capitalize()}:** {value}")
    elif isinstance(content, list):
        for item in content:
            st.write(f"- {item}")
    elif isinstance(content, str):
        st.write(content)
    else:
        st.write("No information available.")

# Function to display a single processed note
def display_note(note, index):
    st.header(f"Note {index}")

    # Define the sections to display
    sections = [
        ("Patient Demographics", "patient_demographics"),
        ("Chief Complaint", "chief_complaint"),
        ("History of Present Illness", "history_of_present_illness"),
        ("Clinical Findings", "clinical_findings"),
        ("Imaging Findings", "imaging_findings"),
        ("Laboratory Results", "laboratory_results"),
        ("Diagnosis", "diagnosis"),
        ("Treatment Plan", "treatment_plan"),
        ("Outcome", "outcome")
    ]

    # Display each section of the note
    for title, key in sections:
        display_section(title, note.get(key, "No information available."))

    st.markdown("---")

# Get example notes if requested
example_notes = get_processed_notes(num_examples, api_key, process=False) if load_examples else []

# Combine example notes with custom note if provided
all_notes = [custom_note] if custom_note else []
all_notes.extend(example_notes)

# Display a warning if no notes are available
if not all_notes:
    st.warning("Please enter a custom note in the sidebar or load example notes for testing.")
else:
    # Create a selectbox for note selection
    note_options = ["Custom Note"] if custom_note else []
    note_options.extend([f"Example Note {i+1}" for i in range(len(example_notes))])
    selected_note_index = st.selectbox("Select a note to preview", range(len(all_notes)), format_func=lambda x: note_options[x])

    # Display the selected note
    st.subheader("Selected Note Preview")
    st.text_area("", value=all_notes[selected_note_index], height=300, disabled=True)

    # Process the selected note when the button is clicked
    if st.button("Process Selected Note"):
        if not api_key:
            st.error("Please enter your OpenAI API Key")
        else:
            with st.spinner("Processing note..."):
                try:
                    processed_note = extract_info_from_notes(all_notes[selected_note_index], api_key)
                    display_note(processed_note, selected_note_index + 1)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Add a footer to the sidebar
st.sidebar.markdown("---")
st.sidebar.write("Created with Streamlit and OpenAI GPT")
