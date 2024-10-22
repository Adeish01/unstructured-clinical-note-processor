from openai import OpenAI
from datasets import load_dataset
from clinical_note import ClinicalNoteSchema, process_structured_info
import json

# Initialize the OpenAI client (we'll pass the API key later)
client = None

# Function to extract information from clinical notes using GPT
def extract_info_from_notes(clinical_note, api_key):
    global client
    # Create a new OpenAI client if the API key has changed
    if client is None or client.api_key != api_key:
        client = OpenAI(api_key=api_key)

    # Use GPT to extract structured information from the clinical note
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",  
        messages=[
            {"role": "system", "content": "Extract the clinical information into structured format."},
            {"role": "user", "content": clinical_note},
        ],
        response_format=ClinicalNoteSchema,
    )   
    
    # Parse the GPT response into a JSON object
    structured_info_JSON = json.loads(completion.choices[0].message.content)
    return structured_info_JSON

# Load clinical notes from the dataset
ds = load_dataset("meowterspace42/clinical_notes")

# Function to get processed or raw clinical notes
def get_processed_notes(num_notes=2, api_key=None, process=True):
    if not api_key:
        raise ValueError("OpenAI API key is required")
    
    notes = []
    for i, note in enumerate(ds['train']):
        if i >= num_notes:
            break
        clinical_note = note['text']
        if process:
            # Process the note using GPT if required
            structured_info = extract_info_from_notes(clinical_note, api_key)
            notes.append(structured_info)
        else:
            # Return the raw note if processing is not required
            notes.append(clinical_note)
    return notes
