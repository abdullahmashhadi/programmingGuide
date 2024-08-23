import os
from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)
c_id=os.getenv("C_SRC_ID")
python_id=os.getenv("PYTHON_SRC_ID")
java_id=os.getenv("JAVA_SRC_ID")
javascript_id=os.getenv("JAVASCRIPT_SRC_ID")
PDF_SOURCE_IDS = {
    "c": c_id,
    "python": python_id,
    "java": java_id,
    "javascript": javascript_id
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
        logging.error(f"Error from API: {response.status_code} {response.text}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

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
        # Return the answer as JSON response
        return jsonify({'answer': answer})
    else:
        return jsonify({'answer': 'An error occurred while processing your request.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
