from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import json
from ..models import db 
from cryptography.fernet import Fernet
import base64
import os

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255))
    processed_content_hash = db.Column(db.Text)  # Contenido hasheado
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    @property
    def _fernet(self):
        """Lazy initialization of Fernet"""
        if not hasattr(self, '_fernet_instance'):
            key = base64.urlsafe_b64encode(hashlib.sha256(current_app.config['SECRET_KEY'].encode()).digest())
            self._fernet_instance = Fernet(key)
        return self._fernet_instance
    
    def set_content(self, content):
        """Encripta el contenido antes de guardarlo"""
        if isinstance(content, dict):
            content = json.dumps(content)
        
        # Encriptar el contenido
        encrypted = self._fernet.encrypt(content.encode())
        self.processed_content_hash = encrypted.decode()
    
    def get_content(self):
        """Desencripta y retorna el contenido original"""
        try:
            if self.processed_content_hash:
                # Desencriptar el contenido
                decrypted = self._fernet.decrypt(self.processed_content_hash.encode())
                return decrypted.decode()
            return None
        except Exception as e:
            current_app.logger.error(f"Error decrypting content: {str(e)}")
            return None