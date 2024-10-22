# Clinical Notes Visualizer

This project is a Streamlit application designed to transform unstructured clinical notes into structured, easily readable information using OpenAI's GPT model. It demonstrates the power of AI in processing and organizing complex medical narratives.

## Features

- Input of unstructured clinical notes (custom or example notes)
- GPT-powered transformation from unstructured text to structured data
- Visualization of processed notes in an organized, easy-to-read format
- Demonstration of AI's capability in medical text processing

## Files

1. `app.py`: The main Streamlit application file.
2. `gpt_medical_info_extractor.py`: Contains functions for processing unstructured clinical notes using GPT.
3. `clinical_note.py`: Defines the schema for structured clinical notes and processing functions.
4. `requirements.txt`: Lists all required Python packages for this project.

## Setup

1. Clone this repository or download the project files.

2. Install the required packages using the `requirements.txt` file:   ```
   pip install -r requirements.txt
   ```

3. Set up an OpenAI API key and keep it handy.

4. Run the Streamlit app:   ```
   streamlit run app.py
   ```

## Usage

1. Enter your OpenAI API key in the sidebar.
2. Input a custom unstructured clinical note or load example notes.
3. Select a note to preview its unstructured format.
4. Click "Process Selected Note" to transform the unstructured text into structured information.
5. View the processed information in an organized, easily readable format.

## How it works

1. Input: The application takes unstructured clinical notes as input. These are typically free-text medical narratives that lack a standardized format.

2. Processing: Using GPT, the app analyzes the unstructured text and extracts relevant medical information.

3. Structuring: The extracted information is organized into predefined categories such as patient demographics, chief complaint, diagnosis, and treatment plan.

4. Output: The structured information is presented in an easy-to-read format, transforming complex medical narratives into clear, organized sections.

This process demonstrates how AI can assist in making medical information more accessible and understandable, potentially improving efficiency in healthcare settings.

## Note

This application is for educational and demonstration purposes only. It should not be used for real medical diagnosis or treatment. Always consult with qualified healthcare professionals for medical advice.

## Created by

This application was created using Streamlit and OpenAI GPT, showcasing the potential of AI in processing and structuring complex medical text.
