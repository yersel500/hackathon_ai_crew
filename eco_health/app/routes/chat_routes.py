# app/routes/chat_routes.py
from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from ..services.pollution_service import PollutionService
from ..models.document import Document 
import requests
import os
from dotenv import load_dotenv
import tiktoken

load_dotenv()

chat_routes = Blueprint('chat_routes', __name__)

# Configuration
API_KEY = os.getenv('AZURE_OPENAI_KEY')
ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')

@chat_routes.route('/api/count-tokens', methods=['POST'])
@login_required
def count_tokens_api():
    try:
        data = request.get_json()
        text = data.get('text', '')
        token_count = count_tokens(text)
        return jsonify({'count': token_count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def count_tokens(text: str) -> int:
    """Count tokens in a text string using tiktoken."""
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    return len(encoding.encode(text))

def get_user_documents_content(user_id):
    """Get processed content from user's documents"""
    documents = Document.query.filter_by(user_id=user_id).all()
    documents_content = []
    for doc in documents:
        content = doc.get_content()
        if content:
            documents_content.append(f"Document '{doc.filename}':\n{content}")
    return documents_content

@chat_routes.route('/api/chat', methods=['POST'])
@login_required
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message')

        input_tokens = count_tokens(user_message)
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        headers = {
            "Content-Type": "application/json",
            "api-key": API_KEY,
        }

        pollution_data = PollutionService().get_local_pollution()

        user_documents = get_user_documents_content(current_user.id)
        documents_context = "\n".join(user_documents) if user_documents else "No documents available"

        system_message = f"""You are an expert health advisor specialized in environmental health and air quality impacts. Your role is to provide personalized health recommendations based on individual medical conditions and current air quality data.

                            Medical Profile:
                            - Conditions: {current_user.medical_condition}
                            - Location: {current_user.location}
                            - Current Air Quality Metrics:
                            {pollution_data}

                            - User documents context: {documents_context}

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
                            5. If the user ask for information of their documents, please provide a detailed information of documents_context

                            Keep responses concise, practical, and focused on the user's specific health conditions and current air quality situation."""

        system_tokens = count_tokens(system_message)

        # Create payload with user context
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": system_message
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
            output_tokens = count_tokens(ai_response)
            total_input_tokens = system_tokens + input_tokens

            session['total_input_tokens'] = session.get('total_input_tokens', 0) + total_input_tokens
            session['total_output_tokens'] = session.get('total_output_tokens', 0) + output_tokens            

            return jsonify({
                'response': ai_response,
                'tokens': {
                    'system': system_tokens,  # Agregar tokens del sistema
                    'user_input': input_tokens,
                    'total_input': total_input_tokens,
                    'output': output_tokens,
                    'total': total_input_tokens + output_tokens,
                    'session_total': {
                        'input': session['total_input_tokens'],
                        'output': session['total_output_tokens'],
                        'total': session['total_input_tokens'] + session['total_output_tokens']
                    }
                }
            })
            
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            return jsonify({'error': 'Failed to get response from AI service'}), 500

    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({'error': str(e)}), 500
    
@chat_routes.route('/api/system-tokens', methods=['GET'])
@login_required
def get_system_tokens():
    try:
        pollution_data = PollutionService().get_local_pollution()
        user_documents = get_user_documents_content(current_user.id)
        documents_context = "\n".join(user_documents) if user_documents else "No documents available"

        system_message = f"""You are an expert health advisor specialized in environmental health and air quality impacts. Your role is to provide personalized health recommendations based on individual medical conditions and current air quality data.

        Medical Profile:
        - Conditions: {current_user.medical_condition}
        - Location: {current_user.location}
        - Current Air Quality Metrics:
        {pollution_data}

        - User documents context: {documents_context}

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

        system_tokens = count_tokens(system_message)
        return jsonify({'system_tokens': system_tokens})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@chat_routes.route('/api/chat/reset-tokens', methods=['POST'])
@login_required
def reset_tokens():
    session['total_input_tokens'] = 0
    session['total_output_tokens'] = 0
    return jsonify({'status': 'success'})