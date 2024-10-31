# app/services/openai_service.py
from openai import OpenAI

class ChatService:
    def __init__(self):
        self.client = OpenAI(
            azure_endpoint="your_azure_openai_endpoint",
            api_key="your_azure_openai_key"
        )

    def get_health_recommendations(self, user_medical_info, pollution_data):
        prompt = f"""
        Given the following medical conditions: {user_medical_info}
        And current pollution levels: {pollution_data}
        
        Provide personalized health recommendations in Spanish, considering:
        1. Current air quality risks
        2. Protective measures
        3. Activities to avoid
        4. When to seek medical attention
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",  # o el modelo que prefieras
            messages=[
                {"role": "system", "content": "Eres un asistente médico especializado en salud ambiental."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content