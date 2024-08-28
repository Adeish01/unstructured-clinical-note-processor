from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from datasets import load_dataset
from clinical_note import ClinicalNoteSchema, process_structured_info
import json

app = Flask(__name__)

# Load clinical notes dataset
print("Loading clinical notes dataset...")
ds = load_dataset("meowterspace42/clinical_notes")
print("Dataset loaded successfully.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_example/<int:index>')
def get_example(index):
    if 0 <= index < len(ds['train']):
        return jsonify({'content': ds['train'][index]['text']})
    return jsonify({'error': 'Invalid index'}), 404

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    api_key = data.get('api_key')

    client = OpenAI(api_key=api_key)
    
    try:
        client = OpenAI(api_key=api_key)

    except Exception as e:
        return jsonify({"error": "Invalid API key"}), 401

    if 'custom_note' in data:
        clinical_note = data['custom_note']
        structured_info = extract_info_from_notes(client, clinical_note)
        return jsonify({
            'unstructured': clinical_note,
            'structured': process_structured_info(structured_info)
        })
    elif 'note_indices' in data:
        results = []
        for index in data['note_indices']:
            clinical_note = ds['train'][index]['text']
            structured_info = extract_info_from_notes(client, clinical_note)
            results.append({
                'unstructured': clinical_note,
                'structured': process_structured_info(structured_info)
            })
        return jsonify({
            'unstructured': [r['unstructured'] for r in results],
            'structured': [r['structured'] for r in results]
        })
    else:
        return jsonify({'error': 'Invalid request'}), 400

def extract_info_from_notes(client, clinical_note):
    print("Sending clinical note to OpenAI for processing...")
    
    # Use the OpenAI GPT API to generate a response
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",  
        messages=[
            {"role": "system", "content": "Extract the clinical information into structured format."},
            {"role": "user", "content": clinical_note},
        ],
        response_format=ClinicalNoteSchema,
    )   
    
    structured_info_JSON = json.loads(completion.choices[0].message.content)
    print("Received structured information from OpenAI.")


    return structured_info_JSON



@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
