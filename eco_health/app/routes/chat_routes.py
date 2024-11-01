# app/routes/chat_routes.py
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..services.pollution_service import PollutionService
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

        pollution_data = PollutionService().get_local_pollution()

        # Create payload with user context
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""You are an expert health advisor specialized in environmental health and air quality impacts. Your role is to provide personalized health recommendations based on individual medical conditions and current air quality data.

                            Medical Profile:
                            - Conditions: {current_user.medical_condition}
                            - Location: {current_user.location}

                            Current Air Quality Metrics:
                            {pollution_data}

                            Instructions:
                            1. Analyze the air quality data and its potential impact on the user's specific medical conditions
                            2. Provide personalized health recommendations, including:
                            - Immediate precautions if needed
                            - Safe outdoor activity recommendations
                            - Indoor air quality tips
                            - Warning signs to watch for
                            - When to seek medical attention
                            3. Explain briefly how the current air quality might affect their specific conditions
                            4. Suggest preventive measures relevant to their medical profile

                            Keep responses concise, practical, and focused on the user's specific health conditions and current air quality situation."""
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