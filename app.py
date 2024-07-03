import os
from flask import Flask, request, jsonify, send_from_directory
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__, static_folder='static')

PDF_SOURCE_IDS = {
    "c": "src_ywH6cZbn1SL1zphBBZBj9",
    # "cpp": "C++.Primer.5th.Edition_2013.pdf",
    "python": "src_6mYivL31UcohIP72KZlGK",
    "java": "src_T64gaP8UcDeBeBgE5y9GW",
    "javascript": "src_as1Gmejb6dRtbuW3ZHbri"
}

def chat_with_pdf(source_id, user_message):
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("No API key found. Please set the API_KEY environment variable in the .env file.")

    headers = {
        'x-api-key': api_key,
        "Content-Type": "application/json",
    }

    data = {
        'sourceId': source_id,
        'messages': [
            {
                'role': "user",
                'content': user_message,
            }
        ]
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

    logging.info(f"API Request to chatpdf: {data}")
    logging.info(f"API Response: {response.status_code} {response.text}")

    if response.status_code == 200:
        return response.json()['content']
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        return None

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    bot = data.get('bot')
    user_input = data.get('userInput')

    source_id = PDF_SOURCE_IDS.get(bot)
    if not source_id:
        return jsonify({'answer': 'Invalid bot selection'}), 400

    answer = chat_with_pdf(source_id, user_input)
    if answer:
        return jsonify({'answer': answer})
    else:
        return jsonify({'answer': 'An error occurred while processing your request.'}), 500