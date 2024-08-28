from typing import List, Optional
from pydantic import BaseModel
import json

# Pydantic model for structured clinical notes
class ClinicalNoteSchema(BaseModel):
    patient_demographics: str
    chief_complaint: Optional[str]
    history_of_present_illness: Optional[str]
    clinical_findings: Optional[str]
    imaging_findings: Optional[str]
    laboratory_results: Optional[str]
    diagnosis: Optional[str]
    treatment_plan: Optional[str]
    outcome: Optional[str]


# Function to process structured information into human-readable text
def process_structured_info(structured_info: json) -> str:
    readable_lines = []

    # Define the labels corresponding to each field in the schema
    keys = [ 
        "patient_demographics",
        "chief_complaint",
        "history_of_present_illness",
        "clinical_findings",
        "imaging_findings",
        "laboratory_results",
        "diagnosis",
        "treatment_plan",
        "outcome"
    ]

    # # Iterate through each field in the structured_info
    for key in keys:
            key_final = key.replace("_", " ")
            value = structured_info[key]
            readable_lines.append(f"{key_final}: {value}")
    human_readable_text = "\n".join(readable_lines)
    
    return human_readable_text