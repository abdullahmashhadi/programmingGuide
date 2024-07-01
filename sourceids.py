import requests
import os
from dotenv import load_dotenv

load_dotenv()

def upload_pdf(file_path):
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("No API key found. Please set the API_KEY environment variable in the .env file.")

    files = [
        ('file', ('file', open(file_path, 'rb'), 'application/octet-stream'))
    ]
    headers = {
        'x-api-key': api_key
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

    if response.status_code == 200:
        return response.json()['sourceId']
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        return None

# Paths to your PDF files
pdf_files = {
    # "c": "c_how_to_program_with_an_introduction_to_c_global_edition_8th_edition.pdf",
    # "cpp": "C++.Primer.5th.Edition_2013.pdf",
    # "python": "Python Basics A Practical Introduction to Python 3-Real Python (2021)-40038.pdf",
    "java": "javanotes5.pdf", 
    # "javascript": "JavaScript-The-Definitive-Guide-6th-Edition.pdf"
}

# Dictionary to store the obtained source IDs
source_ids = {}

# Upload each PDF and store the source ID
for key, file_path in pdf_files.items():
    source_id = upload_pdf(file_path)
    if source_id:
        source_ids[key] = source_id
        print(f"Source ID for {key}: {source_id}")
    else:
        print(f"Failed to upload {file_path}")

# Print all obtained source IDs
print("All source IDs:", source_ids)
