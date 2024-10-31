# app/models/user.py
from datetime import datetime
import json
import os

class User:
    def __init__(self):
        self.users_file = 'users.json'
        # Crear archivo de usuarios si no existe
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

    def create_user(self, user_data):
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            user_id = user_data.get("email")
            users[user_id] = {
                "id": user_id,
                "email": user_data.get("email"),
                "password": user_data.get("password"),  # Debe estar ya hasheado
                "name": user_data.get("name"),
                "medical_conditions": user_data.get("medical_conditions", []),
                "age": user_data.get("age"),
                "location": user_data.get("location"),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            with open(self.users_file, 'w') as f:
                json.dump(users, f)
            
            return users[user_id]
        except Exception as e:
            print(f"Error creating user: {e}")
            raise

    def get_user(self, user_id):
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            return users.get(user_id)
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    def update_user(self, user_id, update_data):
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if user_id not in users:
                raise Exception("User not found")
                
            users[user_id].update(update_data)
            users[user_id]['updated_at'] = datetime.utcnow().isoformat()
            
            with open(self.users_file, 'w') as f:
                json.dump(users, f)
            
            return users[user_id]
        except Exception as e:
            print(f"Error updating user: {e}")
            raise