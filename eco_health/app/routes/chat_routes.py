# app/routes/chat_routes.py
from flask import Blueprint, request, jsonify
from ..services.openai_service import ChatService
from ..services.pollution_service import PollutionService
from ..models.user import User

chat_routes = Blueprint('chat_routes', __name__)
chat_service = ChatService()
user_model = User()

@chat_routes.route('/api/chat/health-advice', methods=['POST'])
def get_health_advice():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        location = data.get('location')
        
        # Obtener información del usuario
        user = user_model.get_user(user_id)
        
        # Obtener datos de contaminación
        pollution_service = PollutionService()
        pollution_data = pollution_service.get_city_pollution(location)
        
        # Obtener recomendaciones
        recommendations = chat_service.get_health_recommendations(
            user['medical_conditions'],
            pollution_data
        )
        
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500