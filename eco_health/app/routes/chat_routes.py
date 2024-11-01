# app/routes/chat_routes.py
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import requests
import os
from dotenv import load_dotenv

load_dotenv()

chat_routes = Blueprint('chat_routes', __name__)

# Configuration
API_KEY = os.getenv('AZURE_OPENAI_KEY')
ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')

@chat_routes.route('/api/chat', methods=['POST'])
@login_required
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        headers = {
            "Content-Type": "application/json",
            "api-key": API_KEY,
        }

        # Create payload with user context
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""You are an AI assistant specialized in environmental health. 
                            The user has the following medical conditions: {current_user.medical_condition}
                            Location: {current_user.location}
                            Provide personalized advice considering their medical conditions and location."""
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_message
                        }
                    ]
                }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 800
        }

        try:
            response = requests.post(ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            
            # Extract the assistant's response from the API response
            ai_response = response.json()['choices'][0]['message']['content']
            return jsonify({'response': ai_response})
            
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            return jsonify({'error': 'Failed to get response from AI service'}), 500

    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({'error': str(e)}), 500